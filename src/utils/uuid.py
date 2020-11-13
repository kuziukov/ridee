import uuid
import random


def generate_uuid1():
    return str(uuid.uuid1())


def generate_code():
    return ''.join(random.sample('0123456789', 6))
