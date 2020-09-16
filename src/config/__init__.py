from .env import (
    DEBUG,
    REDIS_URI
)

TMP_STORE_URI = f'{REDIS_URI}/1'
SESSION_STORE_URI = f'{REDIS_URI}/0'
