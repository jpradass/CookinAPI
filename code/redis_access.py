import redis
import os
from datetime import timedelta

ACCESS_EXPIRES = timedelta(minutes=10)
REFRESH_EXPIRES = timedelta(minutes=60)

revoked_store = redis.StrictRedis(host=os.environ.get('REDIS_HOST', 'localhost'), port=os.environ.get('REDIS_PORT', 6379), password=os.environ.get('REDIS_PWD', '') , username='', db=0, decode_responses=True)