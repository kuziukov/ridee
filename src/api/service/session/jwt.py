import jwt
from datetime import (
    datetime,
    timedelta
)
from aiohttp.web_app import Application
from umongo import Document
from api.service.session import UserSession
from config import Config


class JWTToken(object):
    _alg = 'HS256'

    def __init__(self):
        self._secret = Config.SECRET_KEY

    def generate_access(self, session, expires_in=Config.KEYEXPIRES):
        expires_in = datetime.utcnow() + timedelta(seconds=expires_in)
        payload_access = {
            'id': session.session_id,
            'exp': expires_in,
            'user_id': session.data['user_id'],
        }
        return jwt.encode(payload_access, self._secret, algorithm=self._alg), expires_in

    def generate_refresh(self, session, expires_in=Config.KEYEXPIRES * 2):
        expires_in = datetime.utcnow() + timedelta(seconds=expires_in)
        payload_access = {
            'id': session.session_id,
            'exp': expires_in,
            'user_id': session.data['user_id'],
            'refresh_key': session.data['refresh_key']
        }
        return jwt.encode(payload_access, self._secret, algorithm=self._alg), expires_in

    def parse(self, token):
        payload = jwt.decode(token, self._secret, algorithms=[self._alg])
        return payload


def create_tokens(app: Application, user: Document) -> dict:
    session = await UserSession(app).create_session(user)
    access_token, expires_in = JWTToken().generate_access(session)
    refresh_token, refresh_expires_in = JWTToken().generate_refresh(session)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': expires_in
    }
