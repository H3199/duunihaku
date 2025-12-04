import os
import sys
import tempfile
from pathlib import Path

# Add backend root to sys.path so `api` becomes importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import shutil
import pytest
from sqlmodel import Session, SQLModel, create_engine
from fastapi.testclient import TestClient
from api.main import app

# Copy test db to tmp db.
@pytest.fixture(scope="session")
def test_db_path():
    original = os.path.join(os.path.dirname(__file__), "fixtures/testkanban.db")
    tmp = tempfile.NamedTemporaryFile(delete=False)
    shutil.copyfile(original, tmp.name)
    return tmp.name

@pytest.fixture(scope="session")
def test_engine(test_db_path):
    engine = create_engine(f"sqlite:///{test_db_path}", connect_args={"check_same_thread": False})
    return engine

@pytest.fixture
def override_engine(monkeypatch, test_engine):
    import api.v1.jobs
    monkeypatch.setattr(api.v1.jobs, "engine", test_engine)
    return test_engine


@pytest.fixture
def client(override_engine):
    return TestClient(app)
