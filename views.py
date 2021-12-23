from flask import request, jsonify
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

from db import session
from models import User
from validators import validate_required_fields


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
    return jsonify(user.to_dict('id', 'name'))
