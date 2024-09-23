import redis
from app.core.config import settings
import zlib
import pickle

REDIS_HOST = settings.redis_host
REDIS_PORT = settings.redis_port
REDIS_DB = settings.redis_db

redis_client = None


async def connect_redis():
    global redis_client
    redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

async def read_messages_from_redis(chat_id):
    compresses_json = redis_client.get(chat_id)
    if compresses_json:
        pickled_json = zlib.decompress(compresses_json)
        return pickle.loads(pickled_json)
    return None

async def store_messages_in_redis(chat_id, messages):
    try:
        ttl = settings.redis_ttl
        pickled_json = pickle.dumps(messages)
        compresses_json = zlib.compress(pickled_json)
        redis_client.setex(chat_id, ttl, compresses_json)
    except Exception as e:
        print(f"Error storing messages in Redis: {e}")
