from datetime import date, timedelta

from flask import Flask, jsonify, request
from flask.wrappers import Response

from sqlalchemy import desc, and_, func, text
from sqlalchemy.orm import Query, Session

from src.orm.db_session import DatabaseSession
from src.orm.models import PatientCard, Visit, Diagnosis, visit_diagnoses, Doctor, DoctorSchedule, SickLeave

from src.decorators import require_param, with_session
from src.utils import execute_query_one_or_none, execute_query_all

app = Flask(__name__)


@app.route('/')
def index() -> str:
    return '2024 ETU DB Course Lab 5'


@app.route('/last_visit', methods=['GET'])
@require_param('card_id', int)
@with_session
def last_visit(card_id: int, session: Session) -> Response:
    query: Query = (
        session.query(
            PatientCard.address,
            Visit.date,
            Diagnosis.diagnosis
        )
        .join(Visit, PatientCard.card_id == Visit.card_id)
        .join(visit_diagnoses, Visit.visit_id == visit_diagnoses.c.visit_id)
        .join(Diagnosis, Diagnosis.diagnosis_id == visit_diagnoses.c.diagnosis_id)
        .filter(PatientCard.card_id == card_id)
        .order_by(desc(Visit.date))
        .limit(1)
    )
    return jsonify(execute_query_one_or_none(query))


@app.route('/current_doctor', methods=['GET'])
@require_param('card_id', int)
@with_session
def current_doctor(card_id: int, session: Session) -> Response:
    query = (
        session.query(Doctor.full_name.label('doctor'))
        .join(Visit, Doctor.doctor_id == Visit.doctor_id)
        .filter(Visit.card_id == card_id)
        .order_by(desc(Visit.date))
        .limit(1)
    )
    return jsonify(execute_query_one_or_none(query))


@app.route('/doctor_schedule', methods=['GET'])
@require_param('doctor_id', int)
@with_session
def doctor_schedule(doctor_id: int, session: Session) -> Response:
    query = (
        session.query(
            DoctorSchedule.site_id,
            DoctorSchedule.office,
            DoctorSchedule.weekday,
            DoctorSchedule.begin_time,
            DoctorSchedule.end_time
        )
        .filter(DoctorSchedule.doctor_id == doctor_id)
    )
    return jsonify(execute_query_all(query))


@app.route('/current_patients', methods=['GET'])
@require_param('doctor_id', int)
@with_session
def current_patients(doctor_id: int, session: Session) -> Response:
    query_date = date(2024, 10, 1)
    query = (
        session.query(PatientCard.full_name, SickLeave.sick_leave_end)
        .join(Visit, Visit.card_id == PatientCard.card_id)
        .join(SickLeave, SickLeave.visit_id == Visit.visit_id)
        .filter(SickLeave.sick_leave_end > query_date)
        .filter(Visit.doctor_id == doctor_id)
    )

    return jsonify(execute_query_all(query))


@app.route('/prescriptions', methods=['GET'])
@require_param('diagnosis', str)
@with_session
def prescriptions(diagnosis: str, session: Session) -> Response:
    query = (
        session.query(Diagnosis.prescription)
        .filter(Diagnosis.diagnosis.like(f'%{diagnosis}%'))
    )
    return jsonify(execute_query_all(query))


@app.route('/doctor_in_office', methods=['GET'])
@require_param('office', int)
@with_session
def doctor_in_office(office: int, session: Session) -> Response:
    query_time = '08:00:00'
    query = (
        session.query(Doctor.full_name)
        .join(DoctorSchedule, Doctor.doctor_id == DoctorSchedule.doctor_id)
        .filter(
            and_(
                DoctorSchedule.begin_time <= query_time,
                DoctorSchedule.end_time > query_time,
                DoctorSchedule.office == office
            )
        )
    )

    return jsonify(execute_query_all(query))


@app.route('/visits_amount', methods=['GET'])
@require_param('card_id', int)
@with_session
def visits_amount(card_id: int, session: Session) -> Response:
    one_month_ago = date(2024, 10, 1) - timedelta(days=30)
    query = (
        session.query(func.count(Visit.visit_id).label('visits_amount'))
        .filter(
            and_(
                Visit.card_id == card_id,
                Visit.date >= one_month_ago
            )
        )
    )

    return jsonify(execute_query_one_or_none(query))


@app.route('/doctors_stats', methods=['GET'])
@with_session
def doctor_stats(session: Session) -> Response:
    one_month_ago = date(2024, 10, 1) - timedelta(days=30)
    query = (
        session.query(Doctor.full_name, func.count(Visit.visit_id).label('visits_amount'))
        .outerjoin(Visit, and_(Doctor.doctor_id == Visit.doctor_id, Visit.date >= one_month_ago))
        .group_by(Doctor.full_name)
        .order_by(func.count(Visit.visit_id).desc())
    )

    return jsonify(execute_query_all(query))


@app.route('/unsafe_like', methods=['GET'])
@require_param('name', str)
@with_session
def unsafe(name: str, session: Session) -> Response:
    sql = f"SELECT * FROM patient_card WHERE full_name LIKE '%{name}%'"
    result = session.execute(text(sql))
    return jsonify(execute_query_all(result))


@app.route('/unsafe_int', methods=['GET'])
@with_session
def unsafe_visit(session: Session) -> Response:
    visit_id = request.args.get('visit_id')
    sql = f"SELECT * FROM visit WHERE visit_id >= {visit_id}"
    result = session.execute(text(sql))
    return jsonify(execute_query_all(result))


def main():
    DatabaseSession()

    app.run(host="0.0.0.0", port=5000)


if __name__ == '__main__':
    main()
