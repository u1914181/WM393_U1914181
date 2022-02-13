# Module imports for higher-order funcs that work on other functions.
import functools

# Flask imports required to build web application.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# Used for storing secured passwords with salted hashes.
from werkzeug.security import check_password_hash, generate_password_hash

# Gets instance of the database.
from flaskr.db import get_db

# A blueprint encapsulates functionality such as views and templates.
# These can be applied to the application.
bp = Blueprint('auth', __name__, url_prefix='/auth')

# The first route is admin login.
@bp.route('/admin', methods=('GET', 'POST'))
# The function is called admin.
def admin():
    # To check if theres a post method.
    if request.method == 'POST':
        # Retrieves the username written in the form.
        username = request.form['username']
        # Retrieves the password written in the form.
        password = request.form['password']
        error = None
        # Returns error messages if either of these have been left blank.
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        # If the correct username and password have been entered, successful login message shows and page redirects to the registration page.
        if error is None:
            if username == "admin" and password == "adminpassword":
                print('Successful Login')
                return redirect(url_for('auth.register'))
            else:
                error = 'Incorrect administrative credentials. Please try again.'
        flash(error)
    # If this route can not be followed, the admin template is shown again i.e. if there is an incorrect login.
    return render_template('auth/admin.html')

# The second route is the administrator registering a user.
@bp.route('/register', methods=('GET', 'POST'))
# The function name is register.
def register():
    if request.method == 'POST':
        # Requests the users input.
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        # Connects to the database.
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not role:
            error = 'Role is required. Please enter if student or tutor,'

        if error is None:
            # Tries to insert the collected data into the database.
            try:
                db.execute(
                    "INSERT INTO user (username, password, role) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), role),
                )
                # This is committed to the database.
                db.commit()
            except db.IntegrityError:
                # If the username is already registered, an error is displayed.
                error = f"User {username} is already registered."
            else:
                # If registration is successful, the login page is displayed.
                return redirect(url_for("auth.login"))

        flash(error)
    # If registration is not successful then the registration page is displayed again.
    return render_template('auth/register.html')

# The third route is the login route.
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            # Checks if the data inputted by the user matches the fields in the SQL database.
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
                # If the user is a student, they are directed to the student view of the resource board.
                return redirect(url_for('blog.student_index'))
                print(job)
            elif user[3] == 'Tutor':
                # If the user is a Tutor, they are directed to the Tutor view of the resource board.
                return redirect(url_for('index'))
                print(job)
        flash(error)
    # If incorrect credentials are entered, the login window is displayed again.
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# The logout route clears the session and returns the resource board with no user logged in.
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Login is required to complete many tasks. This function checks that a user is logged in.


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
