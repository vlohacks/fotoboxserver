from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from .auth import login_required

from fotoboxserverapp.db import get_db

import random
import hashlib

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def admin():
    name = ''
    db = get_db()

    # POST = create a new party
    if request.method == 'POST':
        name = request.form['name']
        h = hashlib.sha1()
        # generate some unique but deterministic identifier
        h.update(bytes(name, 'UTF-8'))
        h.update(bytes(current_app.config['SECRET_KEY'], 'UTF-8'))
        d = h.hexdigest()
        # Just use a substring of the identifier 
        # TODO: Map to a alphanumeric identifier to be more user friendly?
        uuid = d[:32]

        db.execute(
            'INSERT INTO feschtla (uuid, name)'
            ' VALUES (?, ?)',
            (uuid, name)
        )

        db.commit()

        return redirect(url_for('admin.admin'))

    
    feschtla = db.execute(
        'SELECT *'
        ' FROM feschtla'
    ).fetchall()

    return render_template('admin.html', feschtla=feschtla, name=name)

@bp.route('/<int:id>/delete')
@login_required
def delete(id):
    db = get_db()
    x = db.execute(
        'DELETE FROM feschtla'
        ' WHERE ID = ?',
        (id, )
    )
    db.commit()

    return redirect(url_for('admin.admin'))


