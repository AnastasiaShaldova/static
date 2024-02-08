from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, UploadFile
from pydantic import PositiveInt
from typing import Optional, List

from app.internal import services
from app.pkg import models

router = APIRouter(prefix="/image", tags=["image"])


@router.post(
    "/",
    response_model=models.StaticIn,
    status_code=status.HTTP_200_OK,
    summary="Upload images.",
)
@inject
async def upload_image(
        cmd: UploadFile,
        static_service: services.StaticDist = Depends(Provide[services.Services.image]),
):
    return await static_service.static_uploader(cmd=cmd)


@router.get(
    "/{image_id:int}",
    response_model=models.ReadSpecificImages,
    status_code=status.HTTP_200_OK,
    summary="Read specific images.",
)
@inject
async def read_image(
        image_id: PositiveInt = models.StaticFields.id,
        static_service: services.StaticDist = Depends(Provide[services.Services.image]),
):
    return await static_service.read_specific_images_by_id(
        query=models.ReadStaticByIdQuery(id=image_id),
    )


@router.get(
    "/",
    response_model=List[models.ReadSpecificImages],
    status_code=status.HTTP_200_OK,
    summary="Get all images."
)
@inject
async def read_all_images(
        static_service: services.StaticDist = Depends(Provide[services.Services.image]),
):
    return await static_service.read_all_specific_images()


@router.delete(
    "/{image_id:int}",
    response_model=models.ReadSpecificImages,
    status_code=status.HTTP_200_OK,
    summary="Delete specific image.",
)
@inject
async def delete_image(
        image_id: PositiveInt = models.StaticFields.id,
        static_service: services.StaticDist = Depends(Provide[services.Services.image]),
):
    return await static_service.delete_specific_image(
        cmd=models.StaticById(id=image_id),
    )


@router.put(
    "/{image_id:int}",
    response_model=Optional[models.ReadSpecificImages],
    status_code=status.HTTP_200_OK,
    summary="Update specific image.",
)
@inject
async def update_image(
        cmd: UploadFile,
        image_id: PositiveInt = models.StaticFields.id,
        static_service: services.StaticDist = Depends(Provide[services.Services.image]),
):
    return await static_service.update_image(cmd=models.UpdateSpecificImages(
        id=image_id,
        image=cmd
    ))
