from dependency_injector import containers, providers

from app.internal.repository.postgresql import Repository
from .image import *


class Services(containers.DeclarativeContainer):
    repository_container = providers.Container(Repository)

    image = providers.Factory(
        StaticDist,
        repository_container.images,
    )
