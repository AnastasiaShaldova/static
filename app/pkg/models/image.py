from fastapi import UploadFile

from pydantic.fields import Field
from pydantic.types import PositiveInt, Optional


from app.pkg.models.base import BaseModel

__all__ = [
    'StaticIn',
    'StaticDist',
    'StaticFields',
    'StaticUpload',
    'ReadSpecificImages',
    'UpdateSpecificImages',
    'ReadStaticByIdQuery',
    'ReadType',
    'StaticById',
]


class StaticFields:
    id = Field(description='id', example=42)
    image_path = Field(description='путь до изображения',
                       example='http://123.48.15.16:2342/static/1664320343_76683e2ddc.jpg')
    image_type_id = Field(description='id type', example=2)
    type_images = Field(description='Тип картинки', example='Аватар')


class BaseStatic(BaseModel):
    """Base model for static."""


class StaticIn(BaseStatic):
    """Model client get in route"""
    id: PositiveInt = StaticFields.id
    image_path: str = StaticFields.image_path


class StaticDist(BaseStatic):
    """Model for work inner project services"""
    image_path: str = StaticFields.image_path


class StaticUpload(BaseStatic):
    """Model for work inner project services with save upload file"""
    image: UploadFile


class ReadSpecificImages(BaseStatic):
    """Model that out in route"""
    id: PositiveInt = StaticFields.id
    image_path: str = StaticFields.image_path

    class Config:
        orm_mode = True


class UpdateSpecificImages(BaseStatic):
    id: PositiveInt = StaticFields.id
    image: UploadFile


class ReadStaticByIdQuery(BaseStatic):
    id: PositiveInt = StaticFields.id


class ReadType(BaseStatic):
    id: PositiveInt = StaticFields.id
    type_images: Optional[str] = StaticFields.type_images


class StaticById(BaseStatic):
    id: PositiveInt = StaticFields.id
