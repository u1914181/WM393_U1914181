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
from flaskr import create_app

'''
The 'test_hello' function is being used to test the example route that was previously created when the flask
application was first made. To test that the web application had been made, I initially added a hello route
and returned 'Hello World' to the HTML page. This test checks that the response matches. This test passed which
means the response data did match.
'''


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
