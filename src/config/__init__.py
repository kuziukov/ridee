from envparse import env


class Config:
    MONGO_URI = env.str('MONGO_URI', default='mongodb://localhost:27017')
    MONGO_DBNAME = env.str('MONGO_DBNAME', default='ridee')
    REDIS_URI = env.str('REDIS_URI', default='redis://127.0.0.1:6379')
    DEBUG = env.str('DEBUG')
    TMP_STORE_URI = f'{REDIS_URI}/1'
    SESSION_STORE_URI = f'{REDIS_URI}/0'
    SECRET_KEY = '0bde8eef5dc532bc3d88e6c2caf5d3cb27b7d591d0cbb5941d7676a2798369a969cf8a6'
    KEYEXPIRES = 2629744


class TestConfig(Config):
    MONGO_URI = env.str('MONGO_TEST_URI', default='mongodb://localhost:27017')
    MONGO_DBNAME = env.str('MONGO_TEST_DBNAME', default='test')
    DEBUG = True
