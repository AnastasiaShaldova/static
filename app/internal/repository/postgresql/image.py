from app.internal.repository.handlers.postgresql.collect_response import (
    collect_response,
)
from app.internal.repository.postgresql.cursor import get_cursor
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = [
    "Static",
]


class Static(Repository):
    @collect_response
    async def create(self, cmd: models.StaticDist) -> models.Static:
        q = """
            insert into images(
                    static_path
            )
                values (
                    %(image_path)s
                )
            returning id;
        """
        async with get_cursor() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.Static) -> models.ReadSpecificImages:
        q = """
                select
                    id, 
                    static_path as image_path
                from images
                where images.id = %(id)s
            """
        async with get_cursor() as cur:
            await cur.execute(q, query.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.Static) -> models.Static:
        q = """
            delete from images where id = %(id)s
            returning id
        """
        async with get_cursor() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def update(self, cmd: models.ReadSpecificImages) -> models.ReadSpecificImages:
        print(f"postgres: {cmd}")
        q = """
            update images 
                set 
                    static_path = %(image_path)s
                where id = %(id)s
            returning 
                id, static_path as image_path;
        """
        async with get_cursor() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()
