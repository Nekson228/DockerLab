from typing import Type
from collections.abc import Iterable, Generator
from itertools import batched

from sqlalchemy.orm import Session

from faker import Faker

from src.orm.base import FakeableBase
from src.orm.models import PatientCard, Visit, Diagnosis, visit_diagnoses, Doctor, DoctorSchedule, SickLeave, Site


def batch_insert(_session: Session,
                 model: Type[FakeableBase],
                 data: Iterable,
                 batch_size: int = 1000) -> None:
    for batch in batched(data, batch_size):
        _session.bulk_insert_mappings(model, batch)
        _session.commit()


def gen_model_fake_data(model: Type[FakeableBase],
                        _faker: Faker,
                        _amount: int) -> Generator[dict, None, None]:
    for _ in range(_amount):
        yield model.fake(_faker).to_dict()


def populate_fake_data(session: Session, amount: int = 10) -> None:
    faker = Faker()
    faker.random_fk = lambda: faker.random_int(min=1, max=amount)

    for model in [Site, Doctor, DoctorSchedule, PatientCard, Visit, SickLeave, Diagnosis]:
        batch_insert(session, model, gen_model_fake_data(model, faker, amount))

    visit_diagnoses_data = []
    visits_ids = [visit_id[0] for visit_id in session.query(Visit.visit_id).all()]
    diagnoses_ids = [diagnosis_id[0] for diagnosis_id in session.query(Diagnosis.diagnosis_id).all()]
    for visit_id in visits_ids:
        visit_diagnoses_data.append({
            'visit_id': visit_id,
            'diagnosis_id': faker.random_sample(diagnoses_ids, length=1)[0]
        })
    session.execute(visit_diagnoses.insert(), visit_diagnoses_data)
    session.commit()
