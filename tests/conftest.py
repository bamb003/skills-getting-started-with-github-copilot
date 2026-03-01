import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(scope="session")
def client():
    """Return a TestClient for the FastAPI app."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities dict before each test."""
    original = copy.deepcopy(activities)
    yield
    # restore
    activities.clear()
    activities.update(original)
