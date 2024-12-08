from datetime import time, date, datetime
from sqlalchemy.orm import Query
from sqlalchemy import Result


def convert_to_serializable(result: dict):
    for key, value in result.items():
        if isinstance(value, (time, date, datetime)):
            result[key] = value.isoformat()
    return result


def execute_query_one_or_none(query: Query | Result) -> dict:
    result = query.one_or_none()
    return convert_to_serializable(dict(result._mapping)) if result else {}


def execute_query_all(query: Query | Result) -> list[dict]:
    return [convert_to_serializable(dict(row._mapping)) for row in query]
