import os
from typing import Union, Optional, List

from fastapi import UploadFile

from app.internal.services.file_handler import upload_file_downloader
from app.pkg.models.exceptions.image import ImageNotFound, TypeNotFound
from app.pkg.models.exceptions.repository import EmptyResult
from app.internal.repository import BaseRepository
from app.internal.repository.postgresql import image
from app.pkg import models
from app.pkg.settings import settings

__all__ = [
    'StaticDist'
]


class StaticDist:
    repository: image.Static

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def static_uploader(
            self,
            cmd: UploadFile,
    ) -> Union[models.StaticIn, models.ReadSpecificImages]:

        image_name = await upload_file_downloader(cmd)
        try:
            return await self.repository.create(models.StaticDist(image_path=image_name))
        except EmptyResult:
            raise ImageNotFound

    async def static_updater(
            self,
            cmd: models.UpdateSpecificImages,
    ) -> models.ReadSpecificImages:

        image_name = await upload_file_downloader(cmd.image)
        try:
            return await self.repository.update(cmd=models.ReadSpecificImages(
                id=cmd.id,
                image_path=image_name)
            )
        except EmptyResult:
            raise ImageNotFound

    async def read_images_by_id(
            self,
            query: models.ReadStaticByIdQuery
    ) -> Union[models.ReadSpecificImages, Exception]:
        """Read specific image from repository by image id."""
        try:
            return await self.repository.read(query=query)
        except EmptyResult:
            raise ImageNotFound

    async def read_all_specific_images(
            self,
            query: Optional[models.ReadAllStaticQuery] = None,
    ) -> List[models.ReadSpecificImages]:
        """Read all images from repository."""
        try:
            if not query:
                query = models.ReadAllStaticQuery()
            return await self.repository.read_all(query=query)
        except EmptyResult:
            raise ImageNotFound

    async def read_specific_images_by_id(
            self,
            query: models.ReadStaticByIdQuery,
    ) -> Union[models.ReadSpecificImages, Exception]:
        """Read specific image from repository by image id."""
        try:
            return await self.repository.read(query=query)
        except EmptyResult:
            raise ImageNotFound

    async def delete_specific_image(
            self,
            cmd: models.StaticById,
    ) -> Union[models.StaticIn, Exception]:
        """Delete specific image from repository by image id."""
        try:
            res = await self.repository.delete(cmd=cmd)
            static_path = res.image_path
            os.remove("." + static_path.split(settings.HOST_PORT.get_secret_value())[-1])
            return res
        except EmptyResult:
            raise ImageNotFound

    async def update_image(
            self,
            cmd: models.UpdateSpecificImages
    ) -> Union[models.ReadSpecificImages, Exception]:
        """Update specific image from repository by image id."""
        try:
            return await self.static_updater(cmd)
        except EmptyResult:
            raise ImageNotFound

    async def read_all_type(
            self,
    ) -> List[models.ReadType]:
        """Read all images from repository."""
        try:
            return await self.repository.read_all()
        except EmptyResult:
            raise TypeNotFound
