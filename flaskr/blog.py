from flask import (
    Blueprint, Flask, flash, g, redirect, render_template, request, url_for, send_file, session
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from werkzeug.utils import secure_filename
import os

bp = Blueprint('blog', __name__)


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
