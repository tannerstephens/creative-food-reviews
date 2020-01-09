from flask import render_template, Blueprint, request

views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template('home.html')
