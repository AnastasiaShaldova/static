from dependency_injector import containers, providers

from app.internal.repository.postgresql import Repository
from .auth_handler import Auth
from .image import *
from .user import *


class Services(containers.DeclarativeContainer):
    repository_container = providers.Container(Repository)

    image = providers.Factory(
        StaticDist,
        repository_container.image,
    )
    auth = providers.Factory(
        Auth
    )
    user = providers.Factory(
        StaticUser,
        repository_container.user,
    )