import pytest
from app.main import create_app
from app.database import db

@pytest.fixture(scope='session')
def app():
    # create an app with testing configuration and in-memory database
    flask_app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    return flask_app

@pytest.fixture(scope='function')
def client(app):
    # create a test client for the app
    return app.test_client()

@pytest.fixture(scope='function', autouse=True)
def db_session(app):
    # database empty and isolated for each test function
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db.session
        db.session.remove()