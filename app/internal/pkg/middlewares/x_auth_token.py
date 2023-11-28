from fastapi import Security
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials

from app.pkg.models.exceptions.x_auth_token import InvalidCredentials, Unauthorized
from app.pkg.settings import settings
from app.internal.services.auth_handler import Auth

__all__ = [
    "get_x_token_key",
    "check_jwt",
    "jwt_header"
]

x_api_key_header = APIKeyHeader(name="X-ACCESS-TOKEN")

jwt_header = HTTPBearer()

auth_handler = Auth()


async def get_x_token_key(
    api_key_header: str = Security(x_api_key_header),
):
    value = settings.X_API_TOKEN_STATIC.get_secret_value()
    if api_key_header != value:
        raise InvalidCredentials


async def check_jwt(
        credentials: HTTPAuthorizationCredentials = Security(jwt_header)
):
    token = credentials.credentials
    if not await auth_handler.verify_token(token):
        raise Unauthorized


