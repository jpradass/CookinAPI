import redis
from datetime import timedelta

ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=1)

revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)