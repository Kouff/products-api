import os

from flask import url_for
from sqlalchemy import *
from sqlalchemy.orm import declarative_base, relationship
from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import config

Base = declarative_base()


class JsonObj:
    def to_dict(self, *fields) -> dict:
        data = {}
        for field in fields:
            data[field] = getattr(self, field, None)
        return data


class ImageObj:
    @property
    def image(self) -> str or None:
        if self.image_filename:
            return url_for('images', model_name=self.__class__.__name__.lower(), name=self.image_filename)
        return None

    def add_image(self, image: FileStorage):
        filename = secure_filename(image.filename)
        dir = os.path.join(config.UPLOAD_FOLDER, self.__class__.__name__.lower(), 'images')
        try:
            image.save(os.path.join(dir, filename))
        except FileNotFoundError:
            os.makedirs(dir)
            image.save(os.path.join(dir, filename))
        self.image_filename = filename


class User(Base, JsonObj, ImageObj):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(150))
    image_filename = Column(String(255))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in kwargs:
            self.set_password(self.password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Product(Base, JsonObj, ImageObj):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    code = Column(String(10))
    name = Column(String(100))
    image_filename = Column(String(255))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")

    def __init__(self, *args, **kwargs):
        image = kwargs.pop('image', None)
        super().__init__(*args, **kwargs)
        if isinstance(image, FileStorage):
            self.add_image(image)


class Price(Base, JsonObj):
    __tablename__ = 'price'
    id = Column(Integer, primary_key=True)
    currency = Column(String(3))
    price = Column(Float)

    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product")
