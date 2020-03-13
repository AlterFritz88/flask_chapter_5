from flask import Flask
from config import Config

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)

from models import Category, User, Dish, db

db.init_app(app)
db.create_all(app=app)
admin = Admin(app=app)


admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Dish, db.session))
admin.add_view(ModelView(User, db.session))

from views import *
from servis_views import *

if __name__ == "__main__":

    app.run()
