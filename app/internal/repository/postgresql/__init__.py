from dependency_injector import containers, providers

from app.pkg.connectors import Connectors

from .image import Static

__all__ = ["Repository"]


class Repository(containers.DeclarativeContainer):
    connectors = providers.Container(Connectors)

    image = providers.Factory(Static, connectors.postgresql)
