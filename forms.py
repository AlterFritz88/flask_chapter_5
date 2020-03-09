from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField
from wtforms.validators import InputRequired, Length, DataRequired, Email


class MakeOrder(FlaskForm):
    name = StringField("Ваше имя", [InputRequired()])
    address = StringField("Адрес", [InputRequired()])
    mail = StringField("Электропочта", [InputRequired(), Email()])
    phone = StringField("Телефон", [InputRequired()])
    submit = SubmitField('Оформить заказ')


class Login(FlaskForm):
    mail = StringField("Электропочта", [InputRequired(), Email()])
    password = PasswordField("Пароль", [InputRequired(), Length(min=5)])
    submit = SubmitField('Войти')


class Registration(FlaskForm):
    mail = StringField("Электропочта", [InputRequired(), Email()])
    password = PasswordField("Пароль", [InputRequired(), Length(min=5)])
    password_1 = PasswordField("Пароль ещё раз", [InputRequired(), Length(min=5)])
    submit = SubmitField('Войти')