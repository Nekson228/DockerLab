from ..base import FakeableBase
from ..types import int_id, weekday
from ..tablenames import DOCTOR_SCHEDULE_TABLE, SITE_TABLE, DOCTOR_TABLE

from datetime import time
from typing import Self, get_args

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from faker import Faker


class DoctorSchedule(FakeableBase):
    __tablename__ = DOCTOR_SCHEDULE_TABLE

    schedule_id: Mapped[int_id]
    site_id: Mapped[int] = mapped_column(ForeignKey(f"{SITE_TABLE}.site_id"))
    doctor_id: Mapped[int] = mapped_column(ForeignKey(f"{DOCTOR_TABLE}.doctor_id"))
    weekday: Mapped[weekday]
    begin_time: Mapped[time]
    end_time: Mapped[time]
    office: Mapped[int]

    site: Mapped["Site"] = relationship(
        back_populates="schedules"
    )
    doctor: Mapped["Doctor"] = relationship(
        back_populates="schedules"
    )

    @classmethod
    def fake(cls, faker: Faker) -> Self:
        begin_time = faker.time_object().replace(minute=0, second=0, microsecond=0)
        if begin_time.hour < 8 or begin_time.hour > 15:
            begin_time = begin_time.replace(hour=8)
        return cls(
            site_id=faker.random_fk(),
            doctor_id=faker.random_fk(),
            weekday=faker.random_element(get_args(weekday)),
            begin_time=begin_time,
            end_time=begin_time.replace(hour=begin_time.hour + 8),
            office=faker.random_int(1, 1000)
        )
