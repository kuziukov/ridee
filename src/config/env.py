from envparse import env

DEBUG = env.str('DEBUG')

REDIS_URI = env.str('REDIS_URI', default='redis://127.0.0.1:6379')


MONGO_URI = env.str('MONGO_URI', default='mongodb://localhost:27017')
MONGO_DBNAME = env.str('MONGO_DBNAME', default='ridee')