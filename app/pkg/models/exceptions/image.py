from fastapi import status
from fastapi.exceptions import HTTPException

from app.pkg.models.base import BaseAPIException

__all__ = [
    "ImageNotFound",
    "FormatError",
]


class ImageNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Image was not found."


class FormatError(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Image must be jpeg."
