# Flask imports required to build web application.
from flask import (
    Blueprint, Flask, flash, g, redirect, render_template, request, url_for, send_file, session
)
# Used for storing secured passwords with salted hashes.

from werkzeug.exceptions import abort
# Imports the other python files to access the logins and database tables.
from flaskr.auth import login_required
from flaskr.db import get_db
from werkzeug.utils import secure_filename
import os

bp = Blueprint('blog', __name__)
# This route returns a message when it is accessed as the functionality has not been included for this assessment.
@bp.route('/blank')
def blank_board():
    return 'This board has been completed by another member of the team and therefore is not included in this project.'


@bp.route('/createboard')
# This route returns a message when it is accessed as the functionality has not been included for this assessment.
def create_board():
    return 'Resource board has been created already. Please contact U1914181 to create another board.'


@bp.route('/edit')
# This route returns a message when it is accessed as the functionality has not been included for this assessment.
def edit_board():
    return 'Board can be edited by: --> Editing resource board uploads using the edit button found on the main board. --> Users can be added providing the users knows the administrative logins.'

# This is the route to the main resource board page for the tutor view.
@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        # There is a dropdown on the page to allow the user to filter the resources shown based upon module.
        module = request.form['module']
        print(module)
        # If the user filters by module, they are directed to another dynamic html file that will contain onlys the resources for that module.
        return redirect(url_for('blog.rating', module=module))
    # Retrieves the database instance.
    db = get_db()
    posts = db.execute(
        # Executes a SQL query to select the data required from the database to be displayed on the html page.
        'SELECT p.id, title, body, body2, module, topic, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    # The resouce board template is rendered including the database queries that have been retrieved.
    return render_template('blog/index.html', posts=posts)

# The student_index is the students view of the resource board.
@bp.route('/student_index', methods=('GET', 'POST'))
def student_index():
    if request.method == 'POST':
        # If the user chooses to filter by module, they will be directed to the html template that dynamically features the resources filtered by module.
        module_student = request.form['module_student']
        print(module_student)
        return redirect(url_for('blog.rating_student', module_student=module_student))
    db = get_db()
    posts = db.execute(
        # Retrieves the required data from the SQL database.
        'SELECT p.id, title, body, body2, module, topic, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/student_index.html', posts=posts)

# This route is for a tutor uploading a resource.
@bp.route('/create', methods=('GET', 'POST'))
# The tutor must be logged in to upload a resource.
@login_required
def create():
    if request.method == 'POST':
        # Retrieves the title, body of text, module and topic that the tutor has entered.
        title = request.form['title']
        print(title)
        print(type(title))
        body = request.form['body']
        rating = request.form['rating']
        print(rating)
        topic = request.form['topic']
        print(topic)
        error = None

        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        # Also retrieves the filename of the resource that the tutor has uploaded.
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            print(os.getcwd())
            # Concantenated the filename to the path to provide the script will a full path ready for download.
            file.save(os.path.join('flaskr\\uploads\\', filename))
            print("saved file successfully")
      # send file name as parameter to downlad
            # return redirect('/downloadfile/' + filename)

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                # Inserts the information into the post table of the SQL database.
                'INSERT INTO post (title, body, author_id, body2, module, topic)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (title, filename, g.user['id'], body, rating, topic)
            )
            db.commit()
            db = get_db()
            error = None
            body_post = db.execute(
                # Selects the filename from the post table.
                'SELECT body2 FROM post WHERE title = ?', (title,)
            ).fetchone()
            body_post2 = body_post[0]

            session[body_post2] = body_post2
            # If the upload has been successful, the tutor is directed back to the resource board.
            return redirect(url_for('blog.index'))
        # If the upload is not succssful, the tutor is directed back to the upload documents view.
    return render_template('blog/create.html')

# Download file route directs the user to the downloads html file.
@bp.route("/downloadfile/<filename>", methods=['GET'])
def download_file(filename):
    return render_template('download.html', value=filename)

# If returns the file that is attached to the resource upload section that they clicked on.
@bp.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = 'uploads\\' + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


def get_post(id, check_author=True):
    post = get_db().execute(
        # Collects all the required information from the SQL database.
        'SELECT p.id, title, body, body2, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    # Error message if resource doesnt exist.
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    # Error message if its not the author attempting to edit the uploaded resource information.
    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

# The update route allows the tutor to edit the title and body of text associated with the uploaded resource.
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    print(post)

    if request.method == 'POST':
        # Retrieves the title and body of text from the user input.
        title = request.form['title']
        body = request.form['body']

        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                # Updates the database if the tutor has updated the resource information.
                'UPDATE post SET title = ?, body2 = ?'
                ' WHERE id = ?',
                (title, body, id,)
            )
            db.commit()
            # If the update is successful then the tutor is directed back to the resource board page.
            return redirect(url_for('blog.index'))
# If the upload is not successful then the tutor is directed back to the update view.
    return render_template('blog/update.html', post=post)

# The delete view allows the tutor to delete an entire upload.
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    # This will also delete the resource information from the post table within the SQL database.
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    # The tutor is then directed back to the resource board.
    return redirect(url_for('blog.index'))

# Route following the tutor filtering the resources shown based upon the module.
@bp.route('/<module>', methods=('GET', 'POST'))
@login_required
def rating(module):
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, body2, module, topic, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE module = ?',
        (module,)
    ).fetchall()
    return render_template('blog/results.html', posts=posts)

# Route following the student filtering the resources shown based upon the module.
@bp.route('/student_index/<module_student>', methods=('GET', 'POST'))
@login_required
def rating_student(module_student):
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, body2, module, topic, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE module = ?',
        (module_student,)
    ).fetchall()
    return render_template('blog/results_student.html', posts=posts)

# Route for student adding a comment to one of the uploaded resources.
@bp.route('/<int:id>/comment', methods=('GET', 'POST'))
@login_required
def comment(id):
    if request.method == 'POST':
        # Collects the title, body of text, module and priority level inputted by the student.
        title = request.form['title']
        body = request.form['body']
        module = request.form['module']
        priority = request.form['priority']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                # Saved to the comments table of the database.
                'INSERT INTO comments (title, body, author_id, module, priority)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, body, g.user['id'], module, priority)
            )
            db.commit()
            # If the comment has been successfully added, the user is directed to the comments page where all the comments are displayed.
            return redirect(url_for('blog.comment_page'))
        # If the comment has not been successfully added, the user is directed back to the add comment view.
    return render_template('blog/comment.html')

# Route for where all the comments are displayed.
@bp.route('/comment_page', methods=('GET', 'POST'))
def comment_page():
    db = get_db()
    comments = db.execute(
        # Data is selected from the database to display in the html file.
        'SELECT c.id, title, body, module, priority, created, author_id, username, reply'
        ' FROM comments c JOIN user u ON c.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/comment_page.html', comments=comments)

# Route for tutor viewing all of the comments and replies that have been added.
@bp.route('/tutor_comment_page', methods=('GET', 'POST'))
def tutor_comment_page():
    db = get_db()
    comments = db.execute(
        # Data is selected from the database to display in the html file.
        'SELECT c.id, title, body, module, priority, created, author_id, username, reply'
        ' FROM comments c JOIN user u ON c.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/tutor_comment_page.html', comments=comments)


def get_comment(id):
    comments = get_db().execute(
        'SELECT id, title, body, module, priority, created, author_id'
        ' FROM comments'
        ' WHERE id = ?',
        (id,)  # Retrieves the comment id.
    ).fetchone()

    return comments

# Route for tutor adding a reply to one of the comments for one of the uploaded resources.
@bp.route('/<int:id>/tutor_reply', methods=('GET', 'POST'))
@login_required
def tutor_reply(id):
    comments = get_comment(id)
    print(comments['title'])

    if request.method == 'POST':
        reply = request.form['reply']
        # Retrieves the reply that the tutor has written.
        print(reply)
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                # Updates the SQL database with the reply.
                'UPDATE comments SET reply = ?'
                ' WHERE id = ?',
                (reply, id,)
            )
            db.commit()
            # Returns the page containing all the comments and replies.
            return redirect(url_for('blog.tutor_comment_page'))

    return render_template('blog/tutor_reply.html', comments=comments)
