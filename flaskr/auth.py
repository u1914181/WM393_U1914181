import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/admin', methods=('GET', 'POST'))
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # role = request.form['role']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            if username == "admin" and password == "adminpassword":
                print('Successful Login')
                return redirect(url_for('auth.register'))
            else:
                error = 'Incorrect administrative credentials. Please try again.'
        flash(error)

    return render_template('auth/admin.html')
