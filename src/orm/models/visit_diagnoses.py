from ..base import Base
from ..tablenames import VISIT_DIAGNOSES_TABLE, VISIT_TABLE, DIAGNOSIS_TABLE

from sqlalchemy import Column, Table, ForeignKey

visit_diagnoses = Table(
    VISIT_DIAGNOSES_TABLE,
    Base.metadata,
    Column("visit_id", ForeignKey(f'{VISIT_TABLE}.visit_id'), primary_key=True),
    Column("diagnosis_id", ForeignKey(f'{DIAGNOSIS_TABLE}.diagnosis_id'), primary_key=True),
)