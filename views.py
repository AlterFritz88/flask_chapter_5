from collections import Counter
from hashlib import md5
from flask import abort, flash, session, redirect, request, render_template, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from models import User, Category, Dish
from forms import MakeOrder, Registration, Login


@app.route('/')
def home():
    dishes_num = len(session.get("cart", []))
    dishes_word = get_dish_num_name(dishes_num)
    categories = db.session.query(Category).all()
    return render_template("main.html", summa=session.get("summa", 0), dishes_num=dishes_num, dishes_word=dishes_word,
                           categories=categories, auth=session.get("is_auth", False))


@app.route('/cart', methods=["POST", "GET"])
def cart():
    dish_list = session.get("cart", [])
    current_sum = session.get("summa", 0)
    if request.method == "POST":
        dish_list.append(request.form.get("dish_id"))
        just_added_dish = db.session.query(Dish).get(request.form.get("dish_id"))
        session["summa"] = current_sum + just_added_dish.price
        session["cart"] = dish_list
        session["cart_action"] = "Блюдо добавлено в корзину"
    dishes_word = get_dish_num_name(len(session.get("cart", [])))
    dish_list = Counter(dish_list)
    dish_list = [(db.session.query(Dish).get(int(x)), y) for x, y in dish_list.most_common()]
    message = session.get("cart_action", "")
    session["cart_action"] = ""
    form = MakeOrder()
    return render_template("cart.html", summa=session.get("summa", 0), dishes_num=len(session.get("cart", [])),
                           dishes_word=dishes_word, dish_list=dish_list, message=message,
                           auth=session.get("is_auth", False), form=form)


@app.route('/make_order', methods=["POST", "GET"])
def make_order():
    if len(session.get("cart", [])) == 0:
        session["cart_action"] = "У Вас нет блюд в корзине"
        return redirect("/cart")

    if not session.get("user"):
        session["cart_action"] = "У Вас нет регистрации тут или Вы не вошли в систему"
        return redirect("/cart")

    form_order = MakeOrder()
    if form_order.validate_on_submit():         # хз почему, но это не работет
        return render_template("ordered.html")
    else:
        errors = []
        if form_order.phone.errors:
            errors += form_order.phone.errors
        if form_order.name.errors:
            errors += form_order.name.errors
        if form_order.address.errors:
            errors += form_order.address.errors
        if not errors:
            return render_template("ordered.html")
        session["cart_action"] = ", ".join(errors)
        return redirect(url_for('.cart'))


@app.route('/auth', methods=["POST", "GET"])
def auth():
    log_form = Login()
    reg_form = Registration()
    return render_template("auth.html", log_form=log_form, reg_form=reg_form, message="")


@app.route('/login', methods=["POST"])
def login():
    log_form = Login()
    reg_form = Registration()

    if log_form.validate_on_submit():
        user = db.session.query(User).filter(User.mail == log_form.mail.data).first()
        if user:
            if user.password_valid(log_form.password.data):
                session["is_auth"] = True
                session["user"] = user.id
                session["mail"] = user.mail
                return redirect(url_for('.account'))
            else:
                return render_template("auth.html", log_form=log_form, reg_form=reg_form,
                                       message="Неверный пароль")
        else:
            return render_template("auth.html", log_form=log_form, reg_form=reg_form, message="Такого пользователя нет",
                                   auth=session.get("is_auth", False))
    else:
        errors = []
        if log_form.mail.errors:
            errors += log_form.mail.errors

        if log_form.password.errors:
            errors += log_form.password.errors
        errors = ", ".join(errors)
        return render_template("auth.html", log_form=log_form, reg_form=reg_form, message=errors)


@app.route('/registration', methods=["POST"])
def registration():
    log_form = Login()
    reg_form = Registration()
    if reg_form.validate_on_submit():
        if reg_form.password.data != reg_form.password_1.data:
            return render_template("auth.html", log_form=log_form, reg_form=reg_form, message="Ошибка в пароле. Пароли не равны")
        if not db.session.query(User).filter(User.mail == reg_form.mail.data).first():
            new_user = User(mail=reg_form.mail.data, address=reg_form.address.data, name=reg_form.name.data,
                            password=reg_form.password.data)
            db.session.add(new_user)
            db.session.commit()
            return render_template("auth.html", log_form=log_form, reg_form=reg_form, message="Пользователь зарегистрирован")
        else:
            return render_template("auth.html", log_form=log_form, reg_form=reg_form,
                                   message="Ошибка регистрации. Такой пользователь уже существует")
    else:
        errors = []
        if reg_form.mail.errors:
            errors += reg_form.mail.errors
        if reg_form.name.errors:
            errors += reg_form.name.errors
        if reg_form.address.errors:
            errors += reg_form.address.errors
        if reg_form.password.errors or reg_form.password_1.errors:
            errors += reg_form.password.errors
        return render_template("auth.html", log_form=log_form, reg_form=reg_form, message=", ".join(errors))


@app.route('/cart_del/<dish_id>', methods=["POST", "GET"])
def del_item_from_cart(dish_id):
    dish_list = [x for x in session.get("cart", []) if x != dish_id]
    session["cart"] = dish_list
    summa = sum([db.session.query(Dish).get(int(x)).price for x in dish_list])
    session["summa"] = summa
    session["cart_action"] = "Блюдо было удалено из корзины"
    return redirect(url_for('.cart'))


@app.route('/account', methods=["POST", "GET"])
def account():
    orders = db.session.query(User.orders).filter(User.id == session["user"]).first()
    print(orders)
    return render_template("account.html", summa=session.get("summa", 0),
                           dishes_num=len(session.get("cart", [])), auth=session.get("is_auth"),
                           dishes_word=get_dish_num_name(len(session.get("cart", []))),
                           orders=orders)


@app.route('/logout', methods=["POST", "GET"])
def logout():
    session["is_auth"] = False
    session["user"] = None
    return redirect(url_for('.home'))


def get_dish_num_name(dishes_num: int) -> str:
    dishes_num = str(dishes_num)[::-1]
    if len(dishes_num) > 1 and (dishes_num[0:2] in ("11", "21", "31", "41", "51")):
        return "блюд"
    elif dishes_num[0] == "1":
        return "блюдо"
    elif dishes_num[0] == "2" or dishes_num[0] == "2" or dishes_num[0] == "3" or dishes_num[0] == "4":
        return "блюда"
    else:
       return "блюд"