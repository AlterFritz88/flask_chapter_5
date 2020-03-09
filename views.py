from collections import Counter

from flask import abort, flash, session, redirect, request, render_template, url_for

from app import app, db
from models import User, Category, Dish
from forms import MakeOrder



@app.route('/')
def home():
    dishes_num = len(session.get("cart", []))
    dishes_word = get_dish_num_name(dishes_num)
    categories = db.session.query(Category).all()
    return render_template("main.html", summa=session.get("summa", 0), dishes_num=dishes_num, dishes_word=dishes_word,
                           categories=categories, auth=session.get("is_auth"))


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
                           auth=session.get("is_auth"), form=form)


@app.route('/make_order', methods=["POST", "GET"])
def make_order():
    if len(session.get("cart", [])) == 0:
        session["cart_action"] = "У Вас нет блюд в корзине"
        return redirect("/cart")

    if not session.get("user_id"):
        session["cart_action"] = "У Вас нет регистрации тут или Вы не вошли в систему"
        return redirect("/cart")

    return render_template("ordered.html")


@app.route('/auth', methods=["POST", "GET"])
def auth():
    return render_template("auth.html")


@app.route('/cart_del/<dish_id>', methods=["POST", "GET"])
def del_item_from_cart(dish_id):
    dish_list = [x for x in session.get("cart", []) if x != dish_id]
    session["cart"] = dish_list
    summa = sum([db.session.query(Dish).get(int(x)).price for x in dish_list])
    session["summa"] = summa
    session["cart_action"] = "Блюдо было удалено из корзины"
    return redirect(url_for('.cart'))


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