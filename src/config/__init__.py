from envparse import env


class Config:
    MONGO_URI = env.str('MONGO_URI', default='mongodb://localhost:27017')
    MONGO_DBNAME = env.str('MONGO_DBNAME', default='ridee')
    REDIS_URI = env.str('REDIS_URI', default='redis://127.0.0.1:6379')
    DEBUG = env.str('DEBUG')
    SESSION_STORE_URI = f'{REDIS_URI}/0'
    TMP_STORE_URI = f'{REDIS_URI}/1'
    WSOCKET_TMP_STORE_URI = f'{REDIS_URI}/2'
    EVENTS_STORE_URI = f'{REDIS_URI}/3'
    SECRET_KEY = '0bde8eef5dc532bc3d88e6c2caf5d3cb27b7d591d0cbb5941d7676a2798369a969cf8a6'
    KEYEXPIRES = 2629744
    TIMBER_ID = "43133"
    TIMBER_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJodHRwczovL2FwaS50aW1iZXIuaW8vIiwiZXhwIjpudWxsLCJpYXQiOjE2MDE4MTIzMjUsImlzcyI6Imh0dHBzOi8vYXBpLnRpbWJlci5pby9hcGlfa2V5cyIsInByb3ZpZGVyX2NsYWltcyI6eyJhcGlfa2V5X2lkIjo0MDAwLCJ1c2VyX2lkIjoiYXBpX2tleXw0MDAwIn0sInN1YiI6ImFwaV9rZXl8NDAwMCJ9.DexD9IVQrtqiBBlbEBqA4jP0xS_FuQQf8TRvOHRcSAo"


class TestConfig(Config):
    MONGO_URI = env.str('MONGO_TEST_URI', default='mongodb://localhost:27017')
    MONGO_DBNAME = env.str('MONGO_TEST_DBNAME', default='test')
    DEBUG = True
