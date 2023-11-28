from fastapi import UploadFile

from app.internal.services.file_handler import upload_file_downloader
from app.pkg.models.exceptions.user import UserNotFound
from app.pkg.models.exceptions.repository import EmptyResult
from app.internal.repository import BaseRepository
from app.internal.repository.postgresql import user
from app.pkg import models


__all__ = [
    'StaticUser'
]


class StaticUser:
    repository: user.StaticUser

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def static_uploader_for_users(
            self,
            load_image: UploadFile,
            cmd: models.StaticTypeImageUserID
    ) -> models.StaticUserUpload:

        image_name = await upload_file_downloader(load_image)
        try:
            return await self.repository.create_static_for_user(models.CreateStaticUserUpload(
                image_path=image_name,
                user_id=cmd.user_id,
                image_type_id=cmd.image_type_id
                )
            )
        except EmptyResult:
            raise UserNotFound
