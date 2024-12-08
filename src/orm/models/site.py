from ..base import FakeableBase
from ..tablenames import SITE_TABLE

from typing import Optional, Self

from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from faker import Faker


class Site(FakeableBase):
    __tablename__ = SITE_TABLE

    site_id: Mapped[int] = mapped_column(primary_key=True)

    patients: Mapped[Optional[list["PatientCard"]]] = relationship(
        back_populates="site"
    )
    schedules: Mapped[Optional[list["DoctorSchedule"]]] = relationship(
        back_populates="site"
    )

    @classmethod
    def fake(cls, faker: Faker) -> Self:
        return cls()
