from os import getenv

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from typing import Optional

from .base import Base


class DatabaseSession:
    _instance: Optional['DatabaseSession'] = None
    _factory: Optional[orm.sessionmaker] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._factory is not None:
            return

        conn_str = getenv("POSTGRES_URL")
        if conn_str is None:
            raise Exception("Environment variable POSTGRES_URL is not set")

        print(f"Connecting to database at {conn_str}...")
        engine = sa.create_engine(conn_str, echo=False)
        self._factory = orm.sessionmaker(bind=engine)

        print("Creating tables...")
        Base.metadata.create_all(engine)
        print("Done!")

    def get_session(self) -> Session:
        if self._factory is None:
            raise Exception("Session factory is not initialized.")
        return self._factory()
