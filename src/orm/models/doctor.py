from ..base import FakeableBase
from ..types import int_id
from ..tablenames import DOCTOR_TABLE

from typing import Optional, Self
from datetime import date

from sqlalchemy.orm import Mapped, relationship, Session

from faker import Faker


class Doctor(FakeableBase):
    __tablename__ = DOCTOR_TABLE

    doctor_id: Mapped[int_id]
    full_name: Mapped[str]
    category: Mapped[str]
    experience_years: Mapped[int]
    birth_day: Mapped[date]

    schedules: Mapped[list["DoctorSchedule"]] = relationship(
        back_populates="doctor"
    )
    visits: Mapped[Optional[list["Visit"]]] = relationship(
        back_populates="doctor"
    )

    @classmethod
    def fake(cls, faker: Faker) -> Self:
        return cls(
            full_name=faker.name(),
            category=faker.word(),
            experience_years=faker.random_int(min=0, max=50),
            birth_day=faker.date_of_birth(minimum_age=25, maximum_age=70),
        )
