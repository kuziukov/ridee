import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY


class Token(object):

    _alg = 'HS256'

    def __init__(self, session_id, user_id):
        self._session_id = str(session_id)
        self._user_id = user_id
        self._exp = None

    @property
    def user_id(self):
        return self._user_id

    @property
    def session_id(self):
        return self._session_id

    def setAlghoritm(self, alg) -> None:
        self._alg = alg

    def generate(self, expires_in, secret=SECRET_KEY) -> (int, str):
        expires_in = datetime.utcnow() + timedelta(seconds=expires_in)
        payload_access = {
            'id': self._session_id,
            'exp': expires_in,
            'user_id': str(self._user_id)
        }
        return jwt.encode(payload_access, secret, algorithm=self._alg), expires_in

    @classmethod
    def parse(cls, token, secret=SECRET_KEY):
        payload = jwt.decode(token, secret, algorithms=[cls._alg])
        token = cls(payload['id'], payload['user_id'])
        expires_in = payload['exp']
        return token, expires_in

    def check(self):
        return True if self.user_id and self.session_id else False