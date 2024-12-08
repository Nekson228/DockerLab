from ..base import FakeableBase
from ..types import int_id
from ..tablenames import DIAGNOSIS_TABLE

from .visit_diagnoses import visit_diagnoses

from typing import Self

from sqlalchemy.orm import Mapped, relationship, Session

from faker import Faker


class Diagnosis(FakeableBase):
    __tablename__ = DIAGNOSIS_TABLE

    diagnosis_id: Mapped[int_id]
    diagnosis: Mapped[str]
    prescription: Mapped[str]

    visits: Mapped[list["Visit"]] = relationship(
        secondary=visit_diagnoses, back_populates="diagnoses"
    )

    @classmethod
    def fake(cls, faker: Faker) -> Self:
        return cls(
            diagnosis=faker.word(),
            prescription=faker.text(),
        )
