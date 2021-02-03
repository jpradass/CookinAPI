import redis
from datetime import timedelta

ACCESS_EXPIRES = timedelta(minutes=10)
REFRESH_EXPIRES = timedelta(minutes=60)

revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)