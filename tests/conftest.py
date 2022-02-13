'''
Module imports of pytest to complete this testing and get_db which is a function previously
defined to obtain an instance of the SQL database connection. 
'''
import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

'''
The SQL database file is saved as data.sql. The code below is opening an instance of this database
in order to retrieve the data within it. 
'''
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    database_data = f.read().decode('utf8')

'''
Comments from __init__.py file to explain the create_app module import.
create_app is the application factory function.
The flask instance is created by app = Flask(__name__, instance_relative_config=True).
__name__ is the current python module.
The instance folder is located outside of the flaskr package and holds the database instance.
app.config.from_mapping() sets some default configurations such as the secret_key and the database (path to db).
app.config.from_pyfile() overrides the default configurations, should this be needed in deployment.
os.makedirs() ensures the instance folder exists.
app.route() creates a simple route to test the app is working.
'''
@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,  # The testing variable is set to true.
        # The database path is defined above in this code.
        'DATABASE': db_path,
    })

    with app.app_context():
        # The database is initialised to provide a connection to the SQL database.
        init_db()
        # The get_db() function provides an instance to the database.
        get_db().executescript(database_data)

    yield app  # The web application is run as part of the tests.

    os.close(db_fd)  # The database connection is closed.
    os.unlink(db_path)


# Tests use the client to make requests to the web application without using the server.
@pytest.fixture
def client(app):
    return app.test_client()  # The web application is referred to using app.


# For the majority of the tests, the user must be logged in.
class AuthActions(object):
    def __init__(self, client):
        # The client is used to make requests without running the server.
        self._client = client

    def login(self, username='TestUsername', password='test'):
        return self._client.post(  # The client is used to make requests without running the server.
            '/auth/login',
            # The POST request retrieves the username and password data.
            data={'username': username, 'password': password}
        )

    # The test is able to logout by accessing the logout view.
    def logout(self):
        # The client is used to make requests without running the server.
        return self._client.get('/auth/logout')


@pytest.fixture
# The client is used to make requests without running the server.
def auth(client):
    # Authentication is required for multiple of the tests created.
    return AuthActions(client)
