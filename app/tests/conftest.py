"""Test client config file."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from app.db.database import Base, get_db
from app.db.models import Dish, Waiter
from app.main import app

engine = create_engine(
    url="sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Redirect request to use testing DB."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def db_session():
    """Fixture to connect with DB."""
    connection = engine.connect()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()


@pytest.fixture(scope="module")
def test_client():
    """Test client initiation for all tests."""
    client = TestClient(app)
    yield client
