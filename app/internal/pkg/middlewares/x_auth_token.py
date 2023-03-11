from fastapi import HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles

from app.pkg.models.exceptions.x_auth_token import InvalidCredentials
from app.pkg.settings import settings

__all__ = [
    "AuthStaticFiles",
    "get_x_token_key",
]

x_api_key_header = APIKeyHeader(name="X-ACCESS-TOKEN")


async def get_x_token_key(
    api_key_header: str = Security(x_api_key_header),
):
    value = settings.X_API_TOKEN_STATIC.get_secret_value()
    if api_key_header != value:
        raise InvalidCredentials


async def verify_x_auth_token(request: Request):
    x_token_headers = [
        i[1] for i in request.headers.raw if i[0].decode("utf-8") == "x-access-token"
    ]
    if x_token_headers:
        x_token = x_token_headers[0].decode("utf-8")
        value = settings.X_API_TOKEN_STATIC.get_secret_value()
        if value == x_token:
            return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated error",
    )


class AuthStaticFiles(StaticFiles):
    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

    async def __call__(self, scope, receive, send) -> None:

        assert scope["type"] == "http"

        request = Request(scope, receive)
        await verify_x_auth_token(request)
        await super().__call__(scope, receive, send)
