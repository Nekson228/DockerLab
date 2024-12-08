from ..base import FakeableBase
from ..types import int_id
from ..tablenames import VISIT_TABLE, PATIENT_CARD_TABLE, DOCTOR_TABLE

from .visit_diagnoses import visit_diagnoses

from typing import Optional, Self
from datetime import date

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from faker import Faker


class Visit(FakeableBase):
    __tablename__ = VISIT_TABLE

    visit_id: Mapped[int_id]
    card_id: Mapped[int] = mapped_column(ForeignKey(f'{PATIENT_CARD_TABLE}.card_id'))
    doctor_id: Mapped[int] = mapped_column(ForeignKey(f'{DOCTOR_TABLE}.doctor_id'))
    date: Mapped[date]
    complaints: Mapped[str]

    patient: Mapped["PatientCard"] = relationship(
        back_populates="visits"
    )
    doctor: Mapped["Doctor"] = relationship(
        back_populates="visits"
    )
    diagnoses: Mapped[list["Diagnosis"]] = relationship(
        secondary=visit_diagnoses, back_populates="visits"
    )
    sick_leave: Mapped[Optional["SickLeave"]] = relationship(
        back_populates="visit"
    )

    @classmethod
    def fake(cls, faker: Faker) -> Self:
        return cls(
            card_id=faker.random_fk(),
            doctor_id=faker.random_fk(),
            date=faker.date_this_century(),
            complaints=faker.text(max_nb_chars=100)
        )
