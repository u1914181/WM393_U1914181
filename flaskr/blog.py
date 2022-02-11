from flask import (
    Blueprint, Flask, flash, g, redirect, render_template, request, url_for, send_file, session
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from werkzeug.utils import secure_filename
import os

bp = Blueprint('blog', __name__)
@bp.route('/blank')
def blank_board():
    return 'This board has been completed by another member of the team and therefore is not included in this project.'


@bp.route('/createboard')
def create_board():
    return 'Resource board has been created already. Please contact U1914181 to create another board.'


@bp.route('/edit')
def edit_board():
    return 'Board can be edited by: --> Editing resource board uploads using the edit button found on the main board. --> Users can be added providing the users knows the administrative logins.'


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, body2, module, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/student_index')
def student_index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, body2, module, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/student_index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
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
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            print(os.getcwd())

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
                'INSERT INTO post (title, body, author_id, body2)'
                ' VALUES (?, ?, ?, ?)',
                (title, filename, g.user['id'], body)
            )
            db.commit()
            db = get_db()
            error = None
            body_post = db.execute(
                'SELECT body2 FROM post WHERE title = ?', (title,)
            ).fetchone()
            body_post2 = body_post[0]
            print('this is it:' + body_post2)

            # print(post[1])
            # print(post[2])
            # print(post[3])
            # print(post[4])
            # print(post[5])

            # return redirect(url_for('blog.index'))
            session[body_post2] = body_post2
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


@bp.route("/downloadfile/<filename>", methods=['GET'])
def download_file(filename):
    return render_template('download.html', value=filename)


@bp.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = 'uploads\\' + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, body2, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    print(post)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        # uploaded_file = request.files['file']
        # filename_upload = uploaded_file.filename
        # print(filename_upload)
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body2 = ?'
                ' WHERE id = ?',
                (title, body, id,)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
