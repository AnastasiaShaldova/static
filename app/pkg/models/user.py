from pydantic.fields import Field
from pydantic.types import PositiveInt, Optional


from app.pkg.models.base import BaseModel

__all__ = [
    'CreateStaticUserUpload',
    'StaticFields',
    'StaticTypeImageUserID',
    'StaticUserFields',
    'StaticUserUpload'
]


class StaticFields:
    id = Field(description='id', example=42)
    image_path = Field(description='путь до изображения',
                       example='http://123.48.15.16:2342/static/1664320343_76683e2ddc.jpg')
    image_type_id = Field(description='id type', example=2)


class StaticUserFields:
    user_id = Field(description='id', example='2')


class BaseStaticUser(BaseModel):
    """Base model for static."""


class StaticUserUpload(BaseStaticUser):
    id: PositiveInt = StaticFields.id
    image_type_id: Optional[PositiveInt] = StaticFields.image_type_id
    user_id: PositiveInt = StaticUserFields.user_id
    image_path: str = StaticFields.image_path


class StaticTypeImageUserID(BaseStaticUser):
    user_id: Optional[PositiveInt] = StaticUserFields.user_id
    image_type_id: Optional[PositiveInt] = StaticFields.image_type_id


class CreateStaticUserUpload(BaseStaticUser):
    image_type_id: PositiveInt = StaticFields.image_type_id
    user_id: PositiveInt = StaticUserFields.user_id
    image_path: str = StaticFields.image_path
