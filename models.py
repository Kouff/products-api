from sqlalchemy import *
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String)
    image_path = Column(String)


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    code = Column(String(10))
    name = Column(String(100))
    image_path = Column(String)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")


class Price(Base):
    __tablename__ = 'price'
    id = Column(Integer, primary_key=True)
    currency = Column(String(3))
    price = Column(Float)

    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product")
