import pytest
from src.main.server.server import create_app_test
from src.drivers.database import db


@pytest.fixture
def app():
    app = create_app_test()
    with app.app_context():
        yield app
        db.drop_all()


@pytest.fixture
def session(app):
    yield db.session
    db.session.rollback()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
