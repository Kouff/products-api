import os
import uuid

from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

import config
from db import session
from models import User
from utils import get_user_from_jwt, check_allowed_image, get_file_extension
from validators import validate_required_fields, validate_fields


@validate_required_fields(dict(name=str, password=str))
def login():
    user = session.query(User).filter(User.name == request.json['name']).first()
    if user and user.check_password(request.json['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify(msg='Invalid name or password.'), 400


@validate_required_fields(dict(name=str, password=str))
def registration():
    user = User(name=request.json['name'], password=request.json['password'])
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        return jsonify(msgs={'name': 'This name is already taken.'}), 400
    return jsonify(user.to_dict('id', 'name', 'image'))


class UsersMeView(MethodView):
    @get_user_from_jwt
    def get(self, user):
        return jsonify(user.to_dict('id', 'name', 'image'))

    @get_user_from_jwt
    @validate_fields(dict(name=str, password=str, image=FileStorage))
    def patch(self, user):
        if 'image' in request.files:
            image = request.files['image']
            if not image or not check_allowed_image(image.filename):
                pass
            image.filename = f'{uuid.uuid4()}.{get_file_extension(image.filename)}'
            user.add_image(image)
        if isinstance(request.json, dict):
            name = request.json.get('name')
            password = request.json.get('password')
            if name:
                user.name = name
            if password:
                user.set_password(password)
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            return jsonify(msgs={'name': 'This name is already taken.'}), 400
        return jsonify(user.to_dict('id', 'name', 'image'))
