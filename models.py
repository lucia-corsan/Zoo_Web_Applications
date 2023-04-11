from . import db
from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

#Por aqui hacemos los modelos de la base de datos

#User in particular also inherits from UserMixin
class User(db.Model, UserMixin):
    # defining the columns of our database
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable = False)
    password = db.Column(db.String(300),nullable=False)
    first_name = db.Column(db.String(150), unique = False, nullable = False)
    role = db.Column(db.Boolean, nullable = False)
    reservations = db.relationship("Reserve", backref="user",lazy=True)

class Reserve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    #sa_id is Specific Activity id
    sa_id = db.Column(db.Integer, db.ForeignKey("activity.id"), nullable=False)
    n_tickets = db.Column(db.Integer, nullable = False)


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #Mete la columna de visible 
    name = db.Column(db.String(200), nullable = False)
    location = db.Column(db.String(200), nullable = False)
    price = db.Column(db.Float, nullable = False)
    date = db.Column(db.DateTime, nullable=False)
    aforo = db.Column(db.Integer, nullable = False)
    featured = db.Column(db.Boolean, nullable = False)
    reservations = db.relationship("Reserve", backref="activity",lazy=True)


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable = False)
    sci_name = db.Column(db.String(200), nullable = False)
    info = db.Column(db.String(20000), nullable = False)






