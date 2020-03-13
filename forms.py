from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField
from wtforms.validators import InputRequired, Length, DataRequired, Email


class MakeOrder(FlaskForm):
    name = StringField("Ваше имя", [InputRequired("Введите имя")])
    address = StringField("Адрес", [InputRequired("Введите адрес")])
    mail = StringField("Электропочта", [InputRequired("Введите емайл"), Email("Это не почта")])
    phone = StringField("Телефон", [InputRequired()])
    submit = SubmitField('Оформить заказ')


class Login(FlaskForm):
    mail = StringField("Электропочта", validators=[DataRequired(message="Нужна почта"), Email(message="Неверная электропочта")])
    password = PasswordField("Пароль", validators=[DataRequired(message="Введите пароль"), Length(min=5, message="Слишком короткий пароль")])
    submit = SubmitField('Войти')


class Registration(FlaskForm):
    mail = StringField("Электропочта", [Email("Неверная электропочта"), InputRequired()])
    password = PasswordField("Пароль", [InputRequired(), Length(min=5, message="Слишком короткий пароль")])
    password_1 = PasswordField("Пароль ещё раз", [InputRequired(), Length(min=5, message="Слишком короткий пароль")])
    name = StringField("Имя", [InputRequired(), Length(min=2, message="Ошибка в имени")])
    address = StringField("Адрес", [InputRequired(), Length(min=5, message="Слишком короткий адрес")])
    submit = SubmitField('Зарегистрироваться')