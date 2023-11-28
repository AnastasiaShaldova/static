import time
from typing import Union
from uuid import uuid4

from fastapi import UploadFile

from app.pkg.models.exceptions.image import FormatError
from app.pkg.settings import settings


async def upload_file_downloader(cmd: UploadFile) -> Union[str, Exception]:
    """Save upload file in static directory and return generate path to instance object"""
    if cmd.content_type not in ['image/jpeg', 'image/png']:
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
