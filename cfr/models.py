from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(current_app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(40), unique=True)
  password_hash = db.Column(db.String(60))
  reviews = db.relationship('Review', backref='user', lazy=True)
  is_admin = db.Column(db.Boolean, default=False)


class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  meal = db.Column(db.String(100))
  text = db.Column(db.Text)
  shortened_text = db.Column(db.String(140))
  image = db.Column(db.String(150))
  rating = db.Column(db.Float)
  source = db.Column(db.String(50))
  date = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def as_dict(self):
    return dict(
      meal=self.meal,
      text=self.text,
      rating=self.rating,
      date=self.date,
      image=self.image
    )
