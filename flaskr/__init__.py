import os

from flask import Flask


def create_website(test_config=None):
    resource_board = Flask(__name__, instance_relative_config=True)
    resource_board.config.from_mapping(
        SECRET_KEY='develop',
        DATABASE=os.path.join(resource_board.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        resource_board.config.from_pyfile('config.py', silent=True)
    else:
        resource_board.config.from_mapping(test_config)

    try:
        os.makedirs(resource_board.instance_path)
    except OSError:
        pass

    @resource_board.route('/test_open')
    def hello():
        return 'Welcome to the resource board!'

    return resource_board
