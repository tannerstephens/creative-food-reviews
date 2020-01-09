from flask import render_template, Blueprint, request, current_app, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from cfr.models import User, db

views = Blueprint('views', __name__)

bcrypt = Bcrypt(current_app)

@current_app.before_request
def pre_request():
  if session.get('user_id'):
    user = User.query.filter_by(id=session.get('user_id'))
  else:
    user = None

  request.user = user

@views.route('/')
def home():
  return render_template('pages/home.html')

@views.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    return render_template('pages/register.html')
  
  username = request.form.get('username')
  password = request.form.get('password')

  if not User.query.filter_by(username=username).first():
    password_hash = bcrypt.generate_password_hash(password)
    user = User(username=username, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('views.home'))

  flash('An error occured during registration, please try again', 'danger')
  
  return render_template('pages/register.html', username=username)

@views.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('pages/login.html')

  username = request.form.get('username')
  password = request.form.get('password')

  user = User.query.filter_by(username=username).first()

  if user and bcrypt.check_password_hash(user.password_hash, password):
    session['user_id'] = user.id
    return redirect(url_for('views.home'))

  flash('Username or password incorrect', 'danger')
  
  return render_template('pages/login.html')

@views.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('views.home'))
