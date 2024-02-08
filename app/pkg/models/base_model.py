import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

__all__ = ["Base", "BaseModel", "BaseIdModel"]

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    def __repr__(self):
        if hasattr(self, 'title'):
            return f'<{self.__class__.__name__}: {self.title}>'
        if hasattr(self, 'name'):
            return f'<{self.__class__.__name__}: {self.name}>'
        return self.repr()

    def repr(self):
        return f'<{self.__class__.__name__}>'


class BaseIdModel(BaseModel):
    __abstract__ = True

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)

    def repr(self):
        return f'<{self.__class__.__name__}: {self.id}>'
