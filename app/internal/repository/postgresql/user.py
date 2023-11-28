from app.internal.repository.handlers.postgresql.collect_response import collect_response
from app.internal.repository.postgresql.connection import get_connect as get_cursor
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = [
    "StaticUser",
]


class StaticUser(Repository):

    @collect_response
    async def create_static_for_user(self, cmd: models.CreateStaticUserUpload) -> models.StaticUserUpload:
        q = """
            WITH user_exists AS (
                SELECT EXISTS(SELECT 1 FROM users WHERE id = %(user_id)s) AS result), 
                    inserted_image AS (
                        INSERT INTO images (static_path) 
                        SELECT %(image_path)s
                        WHERE (SELECT result FROM user_exists)
                        RETURNING id, static_path), 
                    inserted_user_image AS (
                        INSERT INTO users_images (image_id, user_id, type_images_id) 
                        SELECT id, %(user_id)s, %(image_type_id)s 
                        FROM inserted_image
                        RETURNING image_id as id, type_images_id as image_type_id, user_id)
                SELECT 
                    inserted_user_image.id,
                    inserted_user_image.image_type_id,
                    inserted_user_image.user_id,
                    inserted_image.static_path as image_path
                FROM inserted_user_image
                JOIN inserted_image ON inserted_user_image.id = inserted_image.id;
            """
        async with get_cursor() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()
