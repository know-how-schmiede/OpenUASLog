import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

TEST_DB = Path(__file__).parent / "test.db"
os.environ["OPENUASLOG_DATABASE_URL"] = f"sqlite:///{TEST_DB.as_posix()}"
os.environ["OPENUASLOG_SECRET_KEY"] = "test-secret"
os.environ["OPENUASLOG_INITIAL_ADMIN_PASSWORD"] = "admin"

from app.main import app  # noqa: E402
from app.db.database import Base, engine  # noqa: E402


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post("/api/auth/login", json={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
