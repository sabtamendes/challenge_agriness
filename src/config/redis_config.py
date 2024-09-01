import os
import redis
from dotenv import load_dotenv

load_dotenv()

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)



def get_key(key_name):
    full_key = f"batch_{key_name}"
    value = redis_client.get(full_key)
    if value:
        return value
    return None


def update_key(key_name, new_value):
    full_key = f"batch_{key_name}"
    response = redis_client.set(full_key, new_value)
    return response


def delete_key(key_name):
    full_key = f"batch_{key_name}"
    response = redis_client.delete(full_key)
    return response
