import sqlalchemy as sa

from app.pkg.models.base_model import BaseIdModel

__all__ = ['StaticBlockModel']


class StaticBlockModel(BaseIdModel):
    __tablename__ = 'images'
    __table_args__ = {'schema': 'public'}

    image_path = sa.Column(sa.Text)
    is_downloaded = sa.Column(sa.Boolean, nullable=False, default=False)
