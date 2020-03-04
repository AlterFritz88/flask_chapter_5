from flask import Flask
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
db.create_all(app=app)

from views import *

if __name__ == "__main__":
    app.run()