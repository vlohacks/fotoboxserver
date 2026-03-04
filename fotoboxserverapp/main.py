#from crypt import methods
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
from PIL import Image, ExifTags

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

        mergeimage = request.form['mergeimage']

        dir = os.path.join(current_app.config['UPLOAD_DIR'], uuid)

        mergepath = None
        if mergeimage:
            mergepath = os.path.join(current_app.config['MERGE_PICS'], mergeimage)

        if not os.path.isfile(mergepath):
            mergepath = None

        if not os.path.isdir(dir):
            os.mkdir(dir)

        cnt = 0
        while True:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            filename = "{}-{:03d}.jpg".format(timestr, cnt)
            filename_orig = "{}-{:03d}-orig.jpg".format(timestr, cnt)
            thumbname = "{}-{:03d}-thn.jpg".format(timestr, cnt)
            filepath = os.path.join(dir, filename)
            thumbpath = os.path.join(dir, thumbname)
            filepath_orig = os.path.join(dir, filename_orig)
            if (not os.path.isfile(filepath)):
                break
            cnt += 1

        filedata.save(filepath_orig)

        img = Image.open(filedata)

        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break

        exif = img._getexif()

        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 7:
            #img = img.mirror(img)
            img = img.rotate(90, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)

        if mergepath:
            img = img.convert("RGBA")
            width, height = img.size
            mergeimg = Image.open(mergepath)
            mergeimg = mergeimg.resize((width, height), Image.LANCZOS)
            img.alpha_composite(mergeimg, (0, 0))
            img = img.convert("RGB")

        img.save(filepath)

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
