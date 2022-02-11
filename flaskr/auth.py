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


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not role:
            error = 'Role is required. Please enter if student or tutor,'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, role) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), role),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # role = request.form['role']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            print(user[0])
            print(user[1])
            print(user[2])
            print(user[3])
            if user[3] == 'Student':
                return redirect(url_for('blog.student_index'))
                print(job)
            elif user[3] == 'Tutor':
                return redirect(url_for('index'))
                print(job)
        flash(error)

    return render_template('auth/login.html')
