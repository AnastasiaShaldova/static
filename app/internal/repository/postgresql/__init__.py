from dependency_injector import containers, providers

from app.internal.repository.postgresql.image import Static
from app.internal.repository.postgresql.user import StaticUser

__all__ = [
    "Repository",
]


class Repository(containers.DeclarativeContainer):
    image = providers.Factory(Static)
    user = providers.Factory(StaticUser)



