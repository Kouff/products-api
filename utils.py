from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

import config
from db import session
from models import User


def get_user_from_jwt(func):
    @jwt_required()
    def wrapped(*args, **kwargs):
        user_id = get_jwt_identity()
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            return func(*args, user=user, **kwargs)
        return jsonify(jwt='Invalid token.'), 401

    return wrapped


def get_file_extension(filename: str) -> str:
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return ''


def check_allowed_image(filename: str) -> bool:
    return get_file_extension(filename) in config.ALLOWED_IMAGE_EXTENSIONS
