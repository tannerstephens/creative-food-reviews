from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(current_app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(40), unique=True)
  password_hash = db.Column(db.String(60))

class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  slug = db.Column(db.String(40), unique=True)
  meal = db.Column(db.String(100))
  text = db.Column(db.Text)
  image = db.Column(db.String(20))
  rating = db.Column(db.Float)
  source = db.Column(db.String(20))
  date = db.Column(db.DateTime)
  
