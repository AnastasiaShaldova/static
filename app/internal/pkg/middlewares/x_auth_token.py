from dependency_injector.wiring import inject
from fastapi import Security
from fastapi.security import (APIKeyHeader, HTTPAuthorizationCredentials,
                              HTTPBearer)

from app.internal.services.auth_handler import Auth
from app.pkg import models
from app.pkg.models.exceptions.x_auth_token import (InvalidCredentials,
                                                    Unauthorized)
from app.pkg.settings import settings

__all__ = ["get_x_token_key",
           "check_jwt",
           "jwt_header",
           "get_user_id",
           "get_user_role"]

x_api_key_header = APIKeyHeader(name="X-API-TOKEN")

jwt_header = HTTPBearer()

auth_handler = Auth()


async def get_x_token_key(
        api_key_header: str = Security(x_api_key_header),
):
    value = settings.X_API_TOKEN.get_secret_value()
    if api_key_header != value:
        raise InvalidCredentials


async def check_jwt(
        credentials: HTTPAuthorizationCredentials = Security(jwt_header)
):
    token = credentials.credentials
    if not auth_handler.decode_token(token):
        raise Unauthorized


@inject
async def get_user_id(
        credentials: HTTPAuthorizationCredentials = Security(jwt_header)
):
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    if not user_id.get("user_id"):
        raise Unauthorized
    return models.UserID(id=user_id["user_id"])


@inject
async def get_user_role(
        credentials: HTTPAuthorizationCredentials = Security(jwt_header)
):
    token = credentials.credentials
    user = auth_handler.decode_token(token)
    if not user.get("user_id"):
        raise Unauthorized
    return models.User(
        id=user["user_id"],
        is_admin=user["admin"],
        is_moder=user["moder"]
    )
