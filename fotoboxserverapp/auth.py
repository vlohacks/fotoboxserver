import functools
from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from fotoboxserverapp.db import get_db
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user = request.form['user']
        pwd = request.form['pass']

        # only single user called admin...
        # this is NOT how to do it... really.. but hey
        # das isch mit heißer nadel gestrickt...
        if user == 'admin' and check_password_hash(current_app.config['ADMIN_PASSWORD'], pwd):
            session.clear()
            session['loggedin'] = True
            return redirect(url_for('admin.admin'))

        flash('invalid login')

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.admin'))


# decorator for pages requiring login
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('loggedin') != True:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)

    return wrapped_view
