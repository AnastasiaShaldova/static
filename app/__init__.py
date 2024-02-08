"""Main factory builder of ``FastAPI`` server."""
import uvicorn
from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.configuration import __containers__
from app.configuration.server import Server
from app.internal.pkg.middlewares.x_auth_token import get_x_token_key


def create_app() -> FastAPI:
    app = FastAPI(
        dependencies=[Depends(get_x_token_key)],
        title="GoD static"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=False,
    )

    __containers__.allocate_packages(app=app)
    return Server(app).get_app()


if __name__ == '__main__':
    uvicorn.run('app:create_app', reload=True)
