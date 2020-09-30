import jwt
from datetime import (
    datetime,
    timedelta
)
from config import Config


class JWTToken(object):
    _alg = 'HS256'

    def __init__(self):
        self._secret = Config.SECRET_KEY

    def generate(self, session, expires_in=Config.KEYEXPIRES):
        expires_in = datetime.utcnow() + timedelta(seconds=expires_in)
        payload_access = {
            'id': session.key,
            'exp': expires_in,
            'user_id': session.data['user_id'],
        }
        return jwt.encode(payload_access, self._secret, algorithm=self._alg), expires_in

    def parse(self, token):
        payload = jwt.decode(token, self._secret, algorithms=[self._alg])
        return payload

