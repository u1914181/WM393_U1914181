'''
Module imports of pytest to complete this testing and get_db which is a function previously
defined to obtain an instance of the SQL database connection. 
'''
import pytest
from flaskr.db import get_db

'''
In the web application code, there is a decorator function called '@login_required' which ensures
that in order to upload or update a resource, the tutor must be logged in. Also, tutors are only able
to update a resource which belongs to them i.e. they are the author. The purpose of the test below
is to check that a tutor can only update a resource upload that they had previously created.
'''


def test_pytest_author(app, client, auth):
    # Try and change the post author to another user
    with app.app_context():
        # Get the instance of the database.
        db = get_db()
        # Execute the SQL query to attempt to change the author of the uploaded resource.
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')

        db.commit()

    auth.login()
    # User is not allowed to update or delete another users resource therefore if attempted, an error message would be returned.
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # Current user is unable to see the edit link and can therefore not attempt this.
    assert b'href="/1/update"' not in client.get('/').data
