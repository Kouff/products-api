from functools import wraps

from flask import request, jsonify

from utils import get_request_data


def validate_required_fields(required_fields: dict, fields: dict or None = None):
    def validate_required_fields_(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            error_required_fields = []
            error_value_fields = []
            data = get_request_data()
            for field, types in required_fields.items():
                if field not in data:
                    error_required_fields.append(field)
                    continue
                if not isinstance(data[field], types):
                    error_value_fields.append(field)
                    continue
            if fields is not None:
                for field, types in fields.items():
                    if field in data and not isinstance(data[field], types):
                        error_value_fields.append(field)
                        continue
            if error_required_fields or error_value_fields:
                error_data = {}
                for field in error_required_fields:
                    error_data[field] = 'This field is requirement.'
                for field in error_value_fields:
                    error_data[field] = f'The value must be {required_fields[field]}.'
                return jsonify(msgs=error_data), 400
            return func(*args, data=data, **kwargs)

        return wrapped

    return validate_required_fields_


def validate_fields(fields: dict):
    def validate_fields_(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            error_value_fields = []
            data = get_request_data()
            for field, types in fields.items():
                if field in data and not isinstance(data[field], types):
                    error_value_fields.append(field)
                    continue
            if error_value_fields:
                error_data = {}
                for field in error_value_fields:
                    error_data[field] = f'The value must be {fields[field]}.'
                return jsonify(msgs=error_data), 400
            return func(*args, data=data, **kwargs)

        return wrapped

    return validate_fields_
