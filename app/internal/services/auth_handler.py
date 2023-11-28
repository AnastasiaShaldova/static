from datetime import datetime, timedelta
from typing import Any
import jwt
from passlib.context import CryptContext
from app.pkg.models.exceptions import InvalidRefreshToken, RefreshTokenExpired
from app.pkg.settings import settings


class Auth:
    secret = settings.SECRET_KEY_TOKEN.get_secret_value()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def verify_hash_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    async def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def create_access_token(self, user_id: int) -> str:
        exp_access_token_minutes = 30
        payload = {
            'sub': user_id,
            'exp': datetime.utcnow() + timedelta(minutes=exp_access_token_minutes),
            'iat': datetime.utcnow()
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    async def create_refresh_token(self, user_id: int, access_token: Any) -> str:
        exp_refresh_token_hours = 24
        info = access_token[-10:]
        payload = {
            'sub': user_id,
            'exp': datetime.utcnow() + timedelta(hours=exp_refresh_token_hours),
            'iat': datetime.utcnow(),
            'info': info,
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    async def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'], options={"verify_signature": True})
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise RefreshTokenExpired
        except jwt.InvalidTokenError:
            raise InvalidRefreshToken
