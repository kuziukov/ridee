from envparse import env

DEBUG = env.str('DEBUG')

REDIS_URI = env.str('REDIS_URI', default='redis://127.0.0.1:6379')