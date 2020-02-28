from flask import abort, flash, session, redirect, request, render_template

from app import app, db
#from models import User
#from forms import LoginForm, RegistrationForm, ChangePasswordForm


@app.route('/')
def home():
    return render_template("main.html")
