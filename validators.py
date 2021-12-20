from functools import wraps

from flask import request, jsonify


def validate_field(fields: dict):
    def validate_field_(func):
        @wraps(func)
        def wrapped():
            error_required_fields = []
            error_value_fields = []
            data = request.json or {}
            for field, types in fields.items():
                if field not in data:
                    error_required_fields.append(field)
                    continue
                if not isinstance(data[field], types):
                    error_value_fields.append(field)
                    continue
            if error_required_fields or error_value_fields:
                data = {}
                for field in error_required_fields:
                    data[field] = 'This field is requirement.'
                for field in error_value_fields:
                    data[field] = f'The value must be {fields[field]}.'
                return jsonify(data), 400
            return func()

        return wrapped

    return validate_field_
