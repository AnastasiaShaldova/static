from fastapi import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    'ImageNotFound',
    'FormatError',
    'TypeNotFound',
]


class ImageNotFound(BaseAPIException):
    message = "Image not found"
    status_code = status.HTTP_404_NOT_FOUND


class FormatError(BaseAPIException):
    message = "Format is invalid"
    status_code = status.HTTP_400_BAD_REQUEST


class TypeNotFound(BaseAPIException):
    message = "Type not found"
    status_code = status.HTTP_404_NOT_FOUND
