import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

def _get_date():
    return datetime.datetime.now()


class User(db.Model):
    @property
    def password(self):
        return self._password

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    mail = Column(String, nullable=False)
    password_hash = Column(String(), nullable=False)
    address = Column(String, nullable=False)
    orders = relationship("Order", back_populates="user")

    @password.setter
    def password(self, passw):
        self.password_hash = generate_password_hash(passw)

    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)


class Order(db.Model):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=_get_date)
    summa = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")
    dishes = Column(String, nullable=False)


class Dish(db.Model):
    __tablename__ = "dishes"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    picture = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="dishes")


class Category(db.Model):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    dishes = relationship("Dish", back_populates="category")