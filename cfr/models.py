from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(current_app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(40), unique=True)
  password_hash = db.Column(db.String(60))
