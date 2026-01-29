import pytest
import os
from pathlib import Path
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from oniria.__main__ import app
from oniria.infrastructure.db.database import Base, get_session
from oniria.infrastructure.firebase.firebase_service import get_current_external_user
from oniria.application.utils import get_current_user
from oniria.domain.models import User, UserStatus, Plan


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:17") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def engine(postgres_container):
    from sqlalchemy import create_engine

    engine = create_engine(postgres_container.get_connection_url())

    Base.metadata.create_all(bind=engine)

    sql_file = f"{Path(__file__).resolve().parents[1]}/resources/database/oniria.dml"
    if not os.path.isfile(sql_file):
        print(f"Cannot find DML file: {sql_file}")
        return
    with engine.connect() as connection:
        with open(sql_file, "r", encoding="utf-8") as file:
            sql_script = file.read()
            try:
                connection.execute(text(sql_script))
                connection.commit()
                print("DML loaded successfully.")
            except Exception as e:
                print("Error while loading DML:", e)
    return engine


@pytest.fixture
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def mock_external_user():
    return {
        "uid": "user_test_123",
        "email": "test@example.com",
        "name": "Test User",
        "email_verified": True,
    }


@pytest.fixture
def client(db_session):

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    def override_get_current_external_user():
        return mock_external_user

    def override_get_current_user():
        return User(
            uuid="internal_user_123",
            external_uuid="user_test_123",
            dreamer_tag="TestDreamer#1234",
            user_status=UserStatus(name="active"),
            plan=Plan(name="basic", permissions=[]),
            character_sheets=[],
            masters_workshops=[],
        )

    app.dependency_overrides[get_session] = override_get_db
    app.dependency_overrides[get_current_external_user] = (
        override_get_current_external_user
    )
    app.dependency_overrides[get_current_user] = override_get_current_user

    from fastapi.testclient import TestClient

    with TestClient(app) as c:
        yield c
