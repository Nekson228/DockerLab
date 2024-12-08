from functools import wraps
from flask import request, jsonify

from src.orm.db_session import DatabaseSession


def require_param(param_name: str, param_type: type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            param_value = request.args.get(param_name)
            if param_value is None:
                return jsonify({"error": f"'{param_name}' parameter is required"}), 400

            try:
                kwargs[param_name] = param_type(param_value)
            except ValueError:
                return jsonify({"error": f"'{param_name}' must be of type {param_type.__name__}"}), 400

            return func(*args, **kwargs)

        return wrapper

    return decorator


def with_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = DatabaseSession().get_session()
        try:
            kwargs['session'] = session
            return func(*args, **kwargs)
        finally:
            session.close()

    return wrapper
