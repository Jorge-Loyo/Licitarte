"""Fixtures para tests"""
import pytest
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from web.app import app as flask_app
from shared.database.db_manager import DatabaseManager

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db():
    db = DatabaseManager(':memory:')
    yield db
