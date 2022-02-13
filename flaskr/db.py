# SQL and flask module imports.
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

'''
g is used to store data that is relevant for the duration of the request.
current_app directs to the flask application processing the request.
sqlite3.connect() establishes the connection to the sql file.
'''


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # Row means return rows.

    return g.db

# close_db closes the database connection.


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# init_db initialises the database ready for use.


def init_db():
    db = get_db()
    # schema.sql is the name of the sql database created for this project.
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    # Message printed to the terminal.
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db) # flask will call this function after returning a response.
    app.cli.add_command(init_db_command) # adds new command that can be called using flask command.
