from ..base import FakeableBase
from ..types import int_id, sex
from ..tablenames import PATIENT_CARD_TABLE, SITE_TABLE

from typing import Optional, Self
from datetime import date

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import mapped_column, Mapped, relationship, Session

from faker import Faker


class PatientCard(FakeableBase):
    __tablename__ = PATIENT_CARD_TABLE

    card_id: Mapped[int_id]
    site_id: Mapped[int] = mapped_column(ForeignKey(f'{SITE_TABLE}.site_id'))
    full_name: Mapped[str]
    insurance_id: Mapped[int]
    registered_at: Mapped[date]
    address: Mapped[str]
    sex: Mapped[sex]
    age: Mapped[int]

    visits: Mapped[Optional[list["Visit"]]] = relationship(
        back_populates="patient"
    )
    site: Mapped["Site"] = relationship(
        back_populates="patients"
    )

    @classmethod
    def fake(cls, faker: Faker) -> Self:
        return cls(
            full_name=faker.name(),
            site_id=faker.random_fk(),
            insurance_id=faker.random_int(1, 100_000),
            registered_at=faker.date_this_century(),
            address=faker.address(),
            sex=faker.random_sample('MF', length=1)[0],
            age=faker.random_int(1, 100)

        )
