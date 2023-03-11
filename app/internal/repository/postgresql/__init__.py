from dependency_injector import containers, providers

from .image import Static

__all__ = [
    "Repository",
    ]


class Repository(containers.DeclarativeContainer):
    images = providers.Factory(Static)
