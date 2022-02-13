# Module imports required to run tests.
import sqlite3
# get_db is a function defined in the master files.
import pytest
from flaskr.db import get_db

# This function is for testing that the connection is closed after the context.
# This test passed therefore proving the connection was correctly closed.


def test_pytest_get_close_db(app):
    with app.app_context():
        db = get_db() # Get the instance of the database.
        assert db is get_db() # Ensure the connection has been established.

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT Test')

    assert 'closed' in str(e.value)
