from flask import render_template, Blueprint, request, jsonify
from cfr.models import User, Review, db

api = Blueprint('api', __name__, url_prefix='/api')

def success_message(success, **kwargs):
  message = {'success': success}

  for kwarg in kwargs:
    message[kwarg] = kwargs[kwarg]

  return jsonify(message)

@api.route('/userValid/<string:username>')
def check_username(username):
  return success_message(True, available=not bool(User.query.filter_by(username=username).first()))

@api.route('/reviews/<string:meal>')
def get_reviews(meal):
  reviews = Review.query.filter_by(meal=meal).all()

  print(reviews)

  print(repr(meal))

  reviews = list(map(lambda r: r.as_dict(), reviews))

  return success_message(True, reviews=reviews)
