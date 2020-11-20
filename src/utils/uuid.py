import uuid
import random


def generate_uuid1() -> str:
    return str(uuid.uuid1())


def generate_code() -> str:
    return ''.join(random.sample('0123456789', 6))
