# Sets up a temporary test app and database:

import pytest
import os
from app import app as flask_app
from Movie_Web_App.datamanager.models import db

TEST_DB = "test.db"

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{TEST_DB}",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False,
    })

    with flask_app.app_context():
        db.drop_all()
        db.create_all()
    yield flask_app

    # Teardown
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

@pytest.fixture
def client(app):
    return app.test_client()
