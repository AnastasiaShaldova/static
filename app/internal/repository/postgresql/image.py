from typing import List

from sqlalchemy import delete, select, update

from app.pkg.connectors.postgresql import Postgresql
from app.pkg import models
from app.pkg.models.sqlalchemy import StaticBlockModel

__all__ = [
    "Static",
]


class Static:
    postgresql: Postgresql

    def __init__(self, postgresql: Postgresql):
        self.postgresql = postgresql

    async def create(self, cmd: models.StaticDist) -> models.StaticIn:
        as_session = self.postgresql.get_async_session()
        data = cmd.to_dict()
        instance = StaticBlockModel(**data)
        async with as_session() as session:
            async with session.begin():
                session.add(instance)
                await session.commit()
        return models.StaticIn(id=instance.id, image_path=instance.image_path)

    async def read(self, query: models.ReadStaticByIdQuery) -> models.ReadSpecificImages:
        as_session = self.postgresql.get_async_session()
        async with as_session() as session:
            async with session.begin():
                result = await session.execute(select(StaticBlockModel)
                                               .filter(StaticBlockModel.id == query.id))
                result = result.scalars().first()
        if result:
            return models.ReadSpecificImages.from_orm(result)

    async def read_all(self) -> List[models.ReadSpecificImages]:
        as_session = self.postgresql.get_async_session()
        async with as_session() as session:
            async with session.begin():
                result = await session.execute(select(StaticBlockModel)
                                               .order_by(StaticBlockModel.id))
                result = result.scalars().all()
        return [models.ReadSpecificImages.from_orm(item) for item in result]

    async def update(self, cmd: models.ReadSpecificImages) -> models.ReadSpecificImages:
        as_session = self.postgresql.get_async_session()
        async with as_session() as session:
            async with session.begin():
                await session.execute(
                    update(StaticBlockModel)
                    .where(StaticBlockModel.id == cmd.id)
                    .values({'image_path': cmd.image_path})
                )
                await session.commit()
        return models.ReadSpecificImages(id=cmd.id, image_path=cmd.image_path)

    async def delete(self, cmd: models.StaticById) -> models.ReadSpecificImages:
        as_session = self.postgresql.get_async_session()
        async with as_session() as session:
            async with session.begin():
                result = await session.execute(delete(StaticBlockModel)
                                               .filter(StaticBlockModel.id == cmd.id)
                                               .returning(StaticBlockModel))
                result = result.scalars().first()
                await session.commit()
            if result:
                return models.ReadSpecificImages.from_orm(result)
