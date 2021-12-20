from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash

import config
from models import User, Base
from validators import validate_field

engine = create_engine(config.DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = config.SECRET_KEY
jwt = JWTManager(app)


@validate_field(dict(name=str, password=str))
def login():
    user = session.query(User).filter(User.name == request.json['name']).first()
    if user and check_password_hash(user.password, request.json['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify(login='Invalid name or password.'), 400


@validate_field(dict(name=str, password=str))
def registration():
    user = User(name=request.json['name'], password=request.json['password'])
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        return jsonify(name='This name is already taken.'), 400
    return jsonify(access_token='x')


app.add_url_rule('/api/v1/login/', view_func=login, methods=('POST',))
app.add_url_rule('/api/v1/registration/', view_func=registration, methods=('POST',))

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run()
