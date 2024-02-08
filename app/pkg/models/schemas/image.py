from pydantic.types import PositiveInt

from app.pkg.models.base import BaseModel

__all__ = ['BaseStatic']


class BaseStatic(BaseModel):
    id: PositiveInt
    static_path: str
    is_downloaded: bool
