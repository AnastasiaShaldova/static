import time
from typing import Union
from uuid import uuid4

from fastapi import UploadFile
from loguru import logger

from app.pkg.models.exceptions.image import ImageNotFound, FormatError
from app.pkg.models.exceptions.repository import EmptyResult
from app.pkg.settings import settings
from app.internal.repository import BaseRepository
from app.internal.repository.postgresql import image
from app.pkg import models


logger.add('log.json', format='{time} {level} {message}',
           level='INFO',
           rotation='10 MB',
           compression='zip',
           serialize=True)


class StaticDist:
    repository: image.Static

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def upload_file_downloader(self, cmd: UploadFile) -> Union[str, Exception]:

        if cmd.content_type != 'image/jpeg':
            raise FormatError
        else:
            contents = await cmd.read()
            short_uuid = str(uuid4())[-10:]
            image_name = f'{int(time.time())}_{short_uuid}.jpg'
            image_path = settings.DOWNLOAD_PATH + image_name
            with open(image_path, 'wb') as f:
                f.write(contents)
            image_path = f'http://{settings.HOST_URL.get_secret_value()}:{settings.HOST_PORT.get_secret_value()}' \
                         f'/{image_path}'
        return image_path

    async def static_uploader(
            self,
            cmd: UploadFile,
            image_id=None
    ) -> Union[models.Static, models.ReadSpecificImages]:

        image_name = await StaticDist.upload_file_downloader(self, cmd)

        if not image_id:
            return await self.repository.create(models.StaticDist(image_path=image_name))
        else:
            return await self.repository.update(cmd=models.ReadSpecificImages(
                id=image_id,
                image_path=image_name))

    async def read_specific_images_by_id(
            self,
            query: models.Static,
    ) -> Union[models.ReadSpecificImages, Exception]:
        """Read specific image from repository by image id."""
        try:
            return await self.repository.read(query=query)
        except EmptyResult:
            raise ImageNotFound

    async def delete_specific_image(
            self,
            cmd: models.Static,
    ) -> Union[models.Static, Exception]:
        """Delete specific image from repository by image id."""
        try:
            return await self.repository.delete(cmd=cmd)
        except EmptyResult:
            raise ImageNotFound

    async def update_image(
            self,
            cmd: models.UpdateSpecificImages
    ) -> Union[models.ReadSpecificImages, Exception]:
        try:
            return await self.static_uploader(cmd=cmd.image, image_id=cmd.id)
        except EmptyResult:
            raise ImageNotFound
