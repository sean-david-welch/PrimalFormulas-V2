import pytest
import mongomock
from unittest.mock import AsyncMock, patch

from pymongo.errors import (
    DuplicateKeyError,
    OperationFailure,
    ServerSelectionTimeoutError,
)
from fastapi.exceptions import HTTPException


from database.database import database_find_all, database_handle_errors


def test_handle_duplicate_key_error():
    with pytest.raises(HTTPException) as exc_info:
        database_handle_errors(DuplicateKeyError("duplicate key error"))
    assert exc_info.value.status_code == 409
    assert "Duplicate key" in str(exc_info.value.detail)


def test_handle_operation_failure():
    with pytest.raises(HTTPException) as exc_info:
        database_handle_errors(OperationFailure("operation failed"))
    assert exc_info.value.status_code == 500
    assert "Operation failed" in str(exc_info.value.detail)


def test_handle_server_selection_timeout_error():
    with pytest.raises(HTTPException) as exc_info:
        database_handle_errors(ServerSelectionTimeoutError("cannot connect to MongoDB"))
    assert exc_info.value.status_code == 503
    assert "Cannot connect to MongoDB" in str(exc_info.value.detail)


def test_handle_generic_error():
    with pytest.raises(HTTPException) as exc_info:
        database_handle_errors(Exception("generic error"))
    assert exc_info.value.status_code == 500
    assert "Database Operation Failed" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_database_find_all_success():
    mock_cursor = AsyncMock()
    mock_cursor.to_list = AsyncMock(
        return_value=[{"_id": 1, "data": "test1"}, {"_id": 2, "data": "test2"}]
    )

    with patch("app.database.database.database_find_all", return_value=mock_cursor):
        result = await database_find_all(mock_cursor)
        assert len(result) == 2
        assert result[0]["data"] == "test1"
        assert result[1]["data"] == "test2"


@pytest.mark.asyncio
async def test_database_find_all_error():
    collection = mongomock.MongoClient().db.collection

    with pytest.raises(HTTPException) as exc_info:
        await database_find_all(collection)

    assert exc_info.value.status_code == 500
