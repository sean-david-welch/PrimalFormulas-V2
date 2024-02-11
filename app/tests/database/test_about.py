import pytest

from unittest.mock import patch
from mongomock import MongoClient

from app.database.about import get_all_abouts
from app.models.models import AboutContent


@pytest.fixture
async def mock_about_collection():
    client = MongoClient()
    db = client["test_database"]
    collection = db["about_collection"]
    yield collection


@pytest.mark.asyncio
async def test_get_all_abouts(mock_about_collection):
    mock_about_collection.insert_many(
        [{"_id": "1", "content": "Content 1"}, {"_id": "2", "content": "Content 2"}]
    )

    with patch(
        "your_project.database.about.database_find_all",
        return_value=mock_about_collection.find(),
    ) as mock_db_find_all:
        results = await get_all_abouts()

    mock_db_find_all.assert_called_once()

    assert len(list(results)) == 2
