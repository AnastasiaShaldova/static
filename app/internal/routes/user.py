from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, UploadFile
from pydantic import PositiveInt
from typing import Optional

from app.internal import services
from app.pkg import models

router = APIRouter(prefix="/user_image", tags=["User_image"])


@router.post(
    "/upload_image_for_users/{image_type_id:int}/{user_id:int}",
    response_model=Optional[models.StaticUserUpload],
    status_code=status.HTTP_200_OK,
    summary="Upload images.",
)
@inject
async def upload_image_for_users(
        image: UploadFile,
        image_type_id: PositiveInt,
        user_id: PositiveInt,
        user_static_service: services.StaticUser = Depends(Provide[services.Services.user]),
):
    cmd = models.StaticTypeImageUserID(image_type_id=image_type_id, user_id=user_id)
    return await user_static_service.static_uploader_for_users(
        load_image=image,
        cmd=cmd
    )
