'''
Module imports:
os provides functions for creating and removing a directory and retrieving its contents.
Flask is a web framework that allows for the easy development of web applications.
'''
import os

from flask import Flask

'''
create_app is the application factory function.
The flask instance is created by app = Flask(__name__, instance_relative_config=True).
__name__ is the current python module.
The instance folder is located outside of the flaskr package and holds the database instance.
app.config.from_mapping() sets some default configurations such as the secret_key and the database (path to db).
app.config.from_pyfile() overrides the default configurations, should this be needed in deployment.
os.makedirs() ensures the instance folder exists.
app.route() creates a simple route to test the app is working.
'''


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    # Imports the SQL database.
    from . import db
    db.init_app(app)

    from . import auth
    # Registers the blueprint.
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    # All files to upload to the application are saved within the uploads/ folder.
    UPLOAD_FOLDER = 'uploads/'

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # returns the application to the server.
    return app
