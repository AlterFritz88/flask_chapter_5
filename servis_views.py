from flask import abort, flash, session, redirect, request, render_template
from models import Category, Dish
from app import app, db
import csv


@app.route('/fill_db_cats')
def fill_db_cats():
    categories = ["Суши", "Стритфуд", "Пицца", "Паста", "Новинки"]
    for cat in categories:
        categorie = Category(title=cat)
        db.session.add(categorie)
    db.session.commit()
    return "База заполнена"


@app.route("/dish_fill")
def dish_fill():
    def csv_reader(file_obj):
        reader = csv.reader(file_obj)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            else:
                print(row)
                cat = db.session.query(Category).get(int(row[5]))
                dish = Dish(id=int(row[0]), title=row[1], price=int(row[2]), description=row[3], picture=row[4],
                            category_id=row[5],  category=cat)
                db.session.add(dish)
        db.session.commit()

    csv_path = "dishes.csv"
    with open(csv_path, "r") as f_obj:
        csv_reader(f_obj)
    return "Filled"
