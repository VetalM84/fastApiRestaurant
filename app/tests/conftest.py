"""Test client config file."""

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.db.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# These two event listeners are only needed for sqlite for proper
# SAVEPOINT / nested transaction support. Other databases like postgres don't need them.
@event.listens_for(engine, "connect")
def do_connect(dbapi_connection, connection_record):
    """Disable pysqlite's emitting of the BEGIN statement entirely.
    also stops it from emitting COMMIT before any DDL."""
    dbapi_connection.isolation_level = None


@event.listens_for(engine, "begin")
def do_begin(conn):
    """Emit our own BEGIN."""
    conn.exec_driver_sql("BEGIN")


@pytest.fixture()
def session():
    """This fixture is the main difference to before. It creates a nested
    transaction, recreates it when the application code calls session.commit
    and rolls it back at the end."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        """If the application code calls session.commit, it will end the nested
        transaction. Need to start a new one when that happens."""
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


def override_get_db():
    """Redirect request to use testing DB."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def test_app():
    """Test client initiation for all tests."""
    client = TestClient(app)
    yield client
