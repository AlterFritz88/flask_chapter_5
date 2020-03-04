import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship

db = SQLAlchemy()


def _get_date():
    return datetime.datetime.now()


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    mail = Column(String, nullable=False)
    password = Column(String, nullable=False)
    address = Column(String, nullable=False)
    orders = relationship("Order", back_populates="id")


class Dish(db.Model):
    __tablename__ = "dishes"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    picture = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="id")


class Order(db.Model):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=_get_date)
    summa = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    dishes = relationship("Dish", back_populates="title")


class Category(db.Model):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    dishes = relationship("Dish", back_populates="title")