import uuid

from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import FileStorage
from db import session
from models import User, Product, Price
from utils import get_user_from_jwt, check_allowed_image, get_file_extension
from validators import validate_required_fields, validate_fields


@validate_required_fields(dict(name=str, password=str))
def login(data):
    user = session.query(User).filter(User.name == data['name']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify(msg='Invalid name or password.'), 400


@validate_required_fields(dict(name=str, password=str))
def registration(data):
    user = User(name=data['name'], password=data['password'])
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        return jsonify(msgs={'name': 'This name is already taken.'}), 400
    return jsonify(user.to_dict('id', 'name', 'image'))


class MyUserView(MethodView):
    @get_user_from_jwt
    def get(self, user):
        return jsonify(user.to_dict('id', 'name', 'image'))

    @get_user_from_jwt
    @validate_fields(dict(name=str, password=str, image=FileStorage))
    def patch(self, data, user):
        if 'image' in request.files:
            image = request.files['image']
            if not image or not check_allowed_image(image.filename):
                return jsonify(msgs={'image': 'Not allowed extension.'}), 400
            image.filename = f'{uuid.uuid4()}.{get_file_extension(image.filename)}'
            user.add_image(image)
        if data:
            if 'name' in data:
                user.name = data['name']
            if 'password' in data:
                user.set_password(data['password'])
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            return jsonify(msgs={'name': 'This name is already taken.'}), 400
        return jsonify(user.to_dict('id', 'name', 'image'))


class MyProductsView(MethodView):
    @get_user_from_jwt
    def get(self, user):
        products = user.relationship_products
        return jsonify(
            [product.to_dict('id', 'code', 'name', 'image') for product in products]
        )

    @get_user_from_jwt
    @validate_required_fields(dict(code=str, name=str), dict(image=FileStorage))
    def post(self, data, user):
        image = None
        if 'image' in request.files:
            image = request.files['image']
            if not image or not check_allowed_image(image.filename):
                return jsonify(msgs={'image': 'Not allowed extension.'}), 400
            image.filename = f'{uuid.uuid4()}.{get_file_extension(image.filename)}'
        if (data['code'],) in session.query(Product.code).filter(Product.user == user).all():
            return jsonify(msgs={'code': 'This code is already taken.'}), 400
        product = Product(code=data['code'], name=data['name'], image=image, user=user)
        session.add(product)
        try:
            session.commit()
        except IntegrityError:
            return jsonify(msgs={'name': 'This name is already taken.'}), 400
        return jsonify(product.to_dict('id', 'code', 'name', 'image'))


class MyProductDetailView(MethodView):
    def get_product(self, p_id, user):
        return session.query(Product).filter(Product.user == user, Product.id == p_id).first()

    @get_user_from_jwt
    def get(self, p_id, user):
        product = self.get_product(p_id, user)
        if not product:
            return jsonify(msg='Not found.'), 404
        return jsonify(product.to_dict('id', 'code', 'name', 'image', 'prices'))

    @get_user_from_jwt
    @validate_fields(dict(name=str, code=str, image=FileStorage))
    def patch(self, p_id, data, user):
        product = self.get_product(p_id, user)
        if not product:
            return jsonify(msg='Not found.'), 404
        if 'image' in request.files:
            image = request.files['image']
            if not image or not check_allowed_image(image.filename):
                return jsonify(msgs={'image': 'Not allowed extension.'}), 400
            image.filename = f'{uuid.uuid4()}.{get_file_extension(image.filename)}'
            product.add_image(image)
        if data:
            if 'name' in data:
                product.name = data['name']
            if 'code' in data:
                if (data['code'],) in session.query(Product.code).filter(
                        Product.user == user, Product.id != product.id).all():
                    return jsonify(msgs={'code': 'This code is already taken.'}), 400
                product.code = data['code']
        session.add(product)
        session.commit()
        return jsonify(product.to_dict('id', 'code', 'name', 'image', 'prices'))


class MyProductPriceView(MethodView):
    def get_product(self, p_id, user):
        return session.query(Product).filter(Product.user == user, Product.id == p_id).first()

    @get_user_from_jwt
    @validate_required_fields(dict(currency=str, price=(int, float)))
    def post(self, p_id, data, user):
        product = self.get_product(p_id, user)
        if not product:
            return jsonify(msg='Not found.'), 404
        if (data['currency'],) in session.query(Price.currency).filter(
                Price.product == product).all():
            return jsonify(msgs={'currency': 'This currency is already created.'}), 400
        price = Price(currency=data['currency'], price=data['price'], product=product)
        session.add(price)
        session.commit()
        return jsonify(price.to_dict('id', 'currency', 'price', 'product_id'))

