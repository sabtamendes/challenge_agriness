import pytest
from unittest.mock import patch, MagicMock

from src.config.redis_config import get_key, update_key, delete_key


@patch("src.config.redis_config.redis_client")
def test_get_key(mock_redis):

    mock_redis.get.return_value = b"test_value"

    result = get_key("sample_key")

    assert result == b"test_value"
    mock_redis.get.assert_called_once_with("batch_sample_key")


@patch("src.config.redis_config.redis_client")
def test_get_key_not_found(mock_redis):

    mock_redis.get.return_value = None

    result = get_key("sample_key")

    assert result is None
    mock_redis.get.assert_called_once_with("batch_sample_key")


@patch("src.config.redis_config.redis_client")
def test_update_key(mock_redis):

    mock_redis.set.return_value = "OK"

    result = update_key("sample_key", "new_value")

    assert result == "OK"
    mock_redis.set.assert_called_once_with("batch_sample_key", "new_value")


@patch("src.config.redis_config.redis_client")
def test_delete_key(mock_redis):

    mock_redis.delete.return_value = 1

    result = delete_key("sample_key")

    assert result == 1
    mock_redis.delete.assert_called_once_with("batch_sample_key")
