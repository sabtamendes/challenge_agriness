import pytest
import redis
import os
from dotenv import load_dotenv
from src.config.redis_config import get_key, update_key, delete_key

load_dotenv()
@pytest.fixture(scope='module')
def redis_client():
    redis_host = os.getenv("REDIS_HOST")
    redis_port = os.getenv("REDIS_PORT")
    client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    yield client

    client.flushdb()

def test_update_key(redis_client):
    key_name = "test_batch"
    new_value = "test_value"
    
    response = update_key(key_name, new_value)
    assert response is True 

    value = redis_client.get(f"batch_{key_name}")
    assert value == new_value

def test_get_key(redis_client):
    key_name = "test_batch"
    new_value = "test_value"
    
    update_key(key_name, new_value)

    value = get_key(key_name)
    assert value == new_value

def test_delete_key(redis_client):
    key_name = "test_batch"
    new_value = "test_value"
    
    update_key(key_name, new_value)
    
    response = delete_key(key_name)
    assert response == 1 

    value = redis_client.get(f"batch_{key_name}")
    assert value is None
