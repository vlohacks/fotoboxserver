from crypt import methods
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, make_response, current_app, send_file
)

from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash


from fotoboxserverapp.db import get_db

import time
import os
import re
from PIL import Image

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/<string:uuid>/<string:pic>')
def pic(uuid, pic):
    pic = secure_filename(pic)
    uuid = secure_filename(uuid)

    dir = os.path.join(current_app.config['UPLOAD_DIR'], uuid)
    filepath = os.path.join(dir, pic)


    if not os.path.isfile(filepath):
        abort(404)

    return send_file(filepath)        
    


@bp.route('/<string:uuid>', methods=('GET', 'POST'))
def main(uuid):
    db = get_db()

    feschtle = db.execute(
        'SELECT *'
        ' FROM feschtla'
        ' WHERE uuid = ?',
        (uuid,)
    ).fetchone()

    if feschtle is None:
        abort(404, 'not found dude')

    pics = db.execute(
        'SELECT *'
        ' FROM pics'
        ' WHERE fescht_id = ?'
        ' ORDER BY created DESC',
        (feschtle['id'],)
    )


    if request.method == 'POST':
        apikey = request.form['apikey']
        if not check_password_hash(current_app.config['API_KEY'], apikey):
            print(apikey, theapikey)
            abort(404)

        filedata = request.files['filedata']

        dir = os.path.join(current_app.config['UPLOAD_DIR'], uuid)

        if not os.path.isdir(dir):
            os.mkdir(dir)

        cnt = 0
        while True:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            filename = "{}-{:03d}.jpg".format(timestr, cnt) 
            thumbname = "{}-{:03d}-thn.jpg".format(timestr, cnt)
            filepath = os.path.join(dir, filename)
            thumbpath = os.path.join(dir, thumbname)
            if (not os.path.isfile(filename)):
                break
            cnt += 1

        filedata.save(filepath)

        img = Image.open(filedata)
        img.thumbnail((400, 300))
        img.save(thumbpath)

        db.execute(
            'INSERT INTO pics'
            ' (fescht_id, filename, thumbname)'
            ' VALUES (?, ?, ?)',
            (feschtle['id'], filename, thumbname)
        )
        db.commit()

        return make_response("yo", 200)



    return render_template('main.html', feschtle=feschtle, pics=pics)