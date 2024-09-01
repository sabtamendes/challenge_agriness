import pytest
from celery import Celery
from src.server import create_app
from src.init_db import db as _db


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_POOL_SIZE"] = 10
    app.config["SQLALCHEMY_MAX_OVERFLOW"] = 20
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 3600
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

    with app.app_context():
        _db.create_all()
        yield app


@pytest.fixture(scope="function")
def session(app):
    connection = _db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = _db._make_scoped_session(options=options)

    _db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def example_data(session):

    from src.models.batch_model import Batch

    batches = [
        Batch(batch_id="1", status="created", piglet_count=100),
        Batch(batch_id="2", status="created", piglet_count=200),
        Batch(batch_id="3", status="created", piglet_count=150),
    ]
    session.bulk_save_objects(batches)
    session.commit()
