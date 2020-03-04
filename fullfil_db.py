import csv
from models import db, Dish, Category

categories = ["Суши", "Стритфуд", "Пицца", "Паста", "Новинки"]


def csv_reader(file_obj):
    """
    Read a csv file
    """
    reader = csv.reader(file_obj)
    for row in reader:
        print(row)
        #dish = Dish()


def add_cat():
    for cat in categories:
        categorie = Category(title=cat)
        db.session.add(categorie)
    db.session.commit()


if __name__ == "__main__":
    add_cat()

    csv_path = "dishes.csv"
    with open(csv_path, "r") as f_obj:
        csv_reader(f_obj)