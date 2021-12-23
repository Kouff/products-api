from sqlalchemy import *
from sqlalchemy.orm import declarative_base, relationship, Session
from werkzeug.security import generate_password_hash

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(150))
    image_path = Column(String(255))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in kwargs:
            self.set_password(self.password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    code = Column(String(10))
    name = Column(String(100))
    image_path = Column(String(255))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")


class Price(Base):
    __tablename__ = 'price'
    id = Column(Integer, primary_key=True)
    currency = Column(String(3))
    price = Column(Float)

    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product")
