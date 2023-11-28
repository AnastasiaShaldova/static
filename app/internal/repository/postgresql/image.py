from typing import List

from app.internal.repository.handlers.postgresql.collect_response import collect_response
from app.internal.repository.postgresql.connection import get_connect as get_cursor
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = [
    "Static",
]


class Static(Repository):
    @collect_response
    async def create(self, cmd: models.StaticDist) -> models.StaticIn:
        q = """
            INSERT INTO images(
                static_path
            )
                values (
                %(image_path)s
            )
            RETURNING id, static_path as image_path;
        """
        async with get_cursor() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))

            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadStaticByIdQuery) -> models.ReadSpecificImages:
        q = """
            SELECT 
                id, static_path as image_path 
            FROM images
            WHERE 
                images.id = %(id)s
        """
        async with get_cursor() as cur:
            await cur.execute(q, query.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def read_all(self, query: models.ReadAllStaticQuery) -> List[models.ReadSpecificImages]:
        q = """
            SELECT 
                id, static_path as image_path
            FROM images
        """
        async with get_cursor() as cur:
            await cur.execute(q, query.to_dict(show_secrets=True))
            return await cur.fetchall()

    @collect_response
    async def update(self, cmd: models.ReadSpecificImages) -> models.ReadSpecificImages:
        q = """
            UPDATE images
            SET 
                static_path = %(image_path)s
            WHERE 
                id = %(id)s        
            RETURNING 
                id, static_path as image_path;
        """
        async with get_cursor() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.StaticById) -> models.StaticIn:
        q = """
            DELETE FROM images
            WHERE 
                id = %(id)s
            RETURNING id, static_path as image_path;
        """
        async with get_cursor() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def read_all(self, ) -> List[models.ReadType]:
        q = """
            SELECT 
                id, type_images
            FROM type_images
        """
        async with get_cursor() as cur:
            await cur.execute(q)
            return await cur.fetchall()
