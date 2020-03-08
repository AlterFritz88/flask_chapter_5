from collections import Counter

from flask import abort, flash, session, redirect, request, render_template

from app import app, db
from models import User, Category, Dish



@app.route('/')
def home():
    dishes_num = session.get("dishes_num", 0)
    dishes_word = get_dish_num_name(dishes_num)
    categories = db.session.query(Category).all()
    return render_template("main.html", summa=session.get("summa", 0), dishes_num=dishes_num, dishes_word=dishes_word,
                           categories=categories)


@app.route('/cart', methods=["POST", "GET"])
def cart():
    dish_list = session.get("cart", [])
    if request.method == "POST":
        dish_list.append(request.form.get("dish_id"))
        just_added_dish = db.session.query(Dish).get(request.form.get("dish_id"))
        current_sum = session.get("summa", 0)
        session["summa"] = current_sum + just_added_dish.price
        current_dish_num = session.get("dishes_num", 0)
        session["dishes_num"] = current_dish_num + 1
        session["cart"] = dish_list
    dishes_word = get_dish_num_name(session["dishes_num"])
    print(dish_list)
    return render_template("cart.html", summa=session["summa"], dishes_num=session["dishes_num"],
                           dishes_word=dishes_word)


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