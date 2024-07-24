import pytest
from fastapi.testclient import TestClient

from curso_fast.app import app


@pytest.fixture
def client():
    return TestClient(app)
