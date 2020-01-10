import datetime
from flask import render_template, Blueprint, request, current_app, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from cfr.models import User, Review, db
from cfr.lib.imgur import upload_image

views = Blueprint('views', __name__)

bcrypt = Bcrypt(current_app)

@current_app.context_processor
def inject_restaurants():
  return dict(restaurants=current_app.config.get('RESTAURANTS', []))

@current_app.before_request
def pre_request():
  if session.get('user_id'):
    user = User.query.filter_by(id=session.get('user_id')).first()
    if user == None:
      session.clear()
  else:
    user = None

  request.user = user

@views.route('/')
def home():
  upload_image(None)
  page = int(request.args.get('p', 1))

  reviews = Review.query.order_by(Review.date.desc()).paginate(page, 6)

  return render_template('pages/home.html', reviews=reviews)

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

@views.route('/reviews/<int:id>')
def show_review(id):
  review = Review.query.filter_by(id=id).first()

  if not review:
    return redirect(url_for('views.home'))

  return render_template('pages/review.html', review=review)

@views.route('/new', methods=['GET', 'POST'])
def new_review():
  if not request.user:
    return redirect(url_for('views.home'))

  if request.method == 'GET':
    return render_template('pages/edit_review.html')

  meal = request.form.get('meal', '')
  source = request.form.get('source', '')
  other_source = request.form.get('other_source', '')

  review = request.form.get('review', '')
  rating = request.form.get('rating')

  try:
    rating = float(rating)
  except:
    rating = ''

  if not (meal and review and rating and ((source == 'other' and other_source) or (source != 'other' and source))):
    flash('Error submitting review. Verify all required fields are filled.', 'danger')
    return render_template('pages/edit_review.html',
      meal=meal,
      source=source,
      review=review,
      other_source=other_source,
      rating=rating
    )

  if len(meal) > 100 or len(source) > 50:
    flash('There was an error submitting the form.', 'danger')
    return render_template('pages/edit_review.html',
      meal=meal,
      source=source,
      review=review,
      other_source=other_source,
      rating=rating
    )

  if source == 'other':
    source = other_source

  date = datetime.datetime.now()

  if len(review) > 140:
    shortened_text = review[:137] + '...'
  else:
    shortened_text = review[:140]

  image_url = ''

  if 'image' in request.files:
    image = request.files['image'].read()
    if image:
      res = upload_image(image).json()

      if res['status'] == 200:
        image_url = res['data']['link']

  new_review = Review(
    meal=meal,
    source=source,
    rating=rating,
    text=review,
    date=date,
    shortened_text=shortened_text,
    user=request.user,
    image=image_url
  )

  db.session.add(new_review)
  db.session.commit()

  return redirect(url_for('views.home'))
