#This file makes the website folder a python package!
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#creating our database, might have to check the labs again
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app(test_config = None):
    #this is the command to initialize flask
    app = Flask(__name__)
    #This encrypts the cookies and session data related to the website
    #I can choose whatever string as a key so
    app.config['SECRET_KEY'] = 'la mejor web'
    #Cambiar segun los requerimientos del lab4
    #User 23_webapp_25
    #SQL passsword: 7wj24yoZ
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://23_webapp_25:7wj24yoZ@mysql.lab.it.uc3m.es/23_webapp_25a"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    #initializing website
    db.init_app(app)

    #here i indicate where the views files and blueprints are
    from .views import views
    from .auth import auth

    #URL prefix says: All of the files are at this path how do I access them
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    #importar los modelos de la database
    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #telling flask what user we are looking for very basic
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app


def create_database(inp):
    db.drop_all(app=inp)
    db.create_all(app = inp)

    
    print('Created Database!')

