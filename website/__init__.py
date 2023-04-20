from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from distutils.log import debug
from email import message
from sre_constants import SUCCESS
from flask import Flask,render_template,request
from dotenv.main import load_dotenv
import os
load_dotenv()

USER_NAME = os.environ['MAIL_USERNAME']
USER_PASSWORD = os.environ['MAIL_PASSWORD']
SECRET_KEY = os.environ['SECRET_KEY']
print(USER_NAME)
from flask_mail import Mail,Message

db =SQLAlchemy()
mail=Mail()

DB_NAME ="database.db"

def create_app():
    app =Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] =f'sqlite:///{DB_NAME}'
    app.config['MAIL_SERVER'] ='smtp.gmail.com'
    app.config['MAIL_PORT'] =465
    app.config['MAIL_USERNAME']=USER_NAME
    app.config['MAIL_PASSWORD']=USER_PASSWORD
    app.config['MAIL_USE_TLS'] =False
    app.config['MAIL_USE_SSL']=True
    mail.init_app(app)
    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')
    from .models import User,Data
    create_database(app)

    return app
def create_database(app):
    if not path.exists('website/'+DB_NAME):
        db.create_all(app=app)