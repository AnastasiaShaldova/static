"""Server configuration."""
from typing import TypeVar

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.internal.routes import __routes__

__all__ = ["Server"]

from app.pkg.models.base import BaseAPIException
from app.internal.pkg.middlewares.handle_http_exceptions import handle_api_exceptions, handle_internal_exception
from app.pkg.settings import settings

FastAPIInstance = TypeVar("FastAPIInstance", bound="FastAPI")


class Server:

    def __init__(self, app: FastAPI):
        self.__app = app
        self._register_routes(app)
        self._register_http_exceptions(app)
        self._register_distributor(app)

    def get_app(self) -> FastAPIInstance:
        return self.__app

    @staticmethod
    def _register_routes(app: FastAPIInstance) -> None:
        __routes__.allocate_routes(app)

    @staticmethod
    def _register_http_exceptions(app: FastAPIInstance):
        """Register http exceptions.

        FastAPIInstance handle BaseApiExceptions raises inside functions.

        Args:
            app: ``FastAPI`` application instance

        Returns: None
        """

        app.add_exception_handler(BaseAPIException, handle_api_exceptions)
        app.add_exception_handler(Exception, handle_internal_exception)

    @staticmethod
    def _register_distributor(app: FastAPIInstance):
        app.mount(
            "/static",  # ip:port/static/name.png
            StaticFiles(directory=settings.STATIC_PATH),
            name="static",
        )
