from ..base import FakeableBase
from ..types import int_id
from ..tablenames import SICK_LEAVE_TABLE, VISIT_TABLE

from typing import Self
from datetime import date, timedelta

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from faker import Faker


class SickLeave(FakeableBase):
    __tablename__ = SICK_LEAVE_TABLE

    sick_leave_id: Mapped[int_id]
    visit_id: Mapped[int] = mapped_column(ForeignKey(f'{VISIT_TABLE}.visit_id'))
    sick_leave_begin: Mapped[date]
    sick_leave_end: Mapped[date]

    visit: Mapped["Visit"] = relationship(
        back_populates="sick_leave"
    )

    @classmethod
    def fake(cls, faker: Faker) -> Self:
        sick_leave_begin = faker.date_this_century()
        return cls(
            visit_id=faker.random_fk(),
            sick_leave_begin=sick_leave_begin,
            sick_leave_end=sick_leave_begin + timedelta(days=faker.random_int(3, 90))
        )
