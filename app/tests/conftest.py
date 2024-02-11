import pytest
from mongomock import MongoClient
from database.database import collections


@pytest.fixture
async def mock_about_collection():
    client = MongoClient()
    db = client["test_database"]
    collections["about"] = db["about_collection"]
    yield collections["about"]
