import jwt

from app.pkg.models.exceptions import (InvalidScopeToken, InvalidToken,
                                       TokenExpired)
from app.pkg.settings import settings


class Auth:
    secret = settings.SECRET_KEY_TOKEN.get_secret_value()

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if payload['scope'] == 'access_token':
                return payload
            raise InvalidScopeToken
        except jwt.ExpiredSignatureError:
            raise TokenExpired
        except jwt.InvalidTokenError:
            raise InvalidToken
