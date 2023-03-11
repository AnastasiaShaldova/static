from fastapi import UploadFile
from app.pkg.models.base import BaseModel
from pydantic.fields import Field
from pydantic.types import PositiveInt


__all__ = [
    'Static',
    'StaticDist',
    'StaticFields',
    'StaticUpload',
    'ReadSpecificImages',
    'UpdateSpecificImages',
]


class StaticFields:
    id = Field(description="id изображения", example=42)
    image_path = Field(description="путь до изображения",
                       example='http://123.48.15.16:2342/static/1664320343_76683e2ddc.jpg')


class BaseStatic(BaseModel):
    """Base model for static."""


class Static(BaseStatic):
    id: PositiveInt = StaticFields.id


class StaticDist(BaseStatic):
    image_path: str = StaticFields.image_path


class StaticUpload(BaseStatic):
    image: UploadFile


class ReadSpecificImages(BaseStatic):
    id: PositiveInt = StaticFields.id
    image_path: str = StaticFields.image_path


class UpdateSpecificImages(BaseStatic):
    id: PositiveInt = StaticFields.id
    image: UploadFile
