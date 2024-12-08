from abc import abstractmethod

from sqlalchemy.orm import DeclarativeBase, Session

from faker import Faker


class Base(DeclarativeBase):
    __abstract__ = True
    pass


class FakeableBase(Base):
    __abstract__ = True

    @classmethod
    @abstractmethod
    def fake(cls, faker: Faker) -> "FakeableBase": ...

    def to_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
