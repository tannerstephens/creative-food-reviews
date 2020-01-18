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
  if request.user:
    return redirect(url_for('views.home'))

  if request.method == 'GET':
    return render_template('pages/register.html')
  
  username = request.form.get('username', '').lower()
  password = request.form.get('password')

  if not User.query.filter(User.username.ilike(username)).first():
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

  user = User.query.filter(User.username.ilike(username)).first()

  if user and bcrypt.check_password_hash(user.password_hash, password):
    session['user_id'] = user.id
    return redirect(url_for('views.home'))

  flash('Username or password incorrect', 'danger')
  
  return render_template('pages/login.html')

@views.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('views.home'))

def create_or_update_review(review=None):
  meal = request.form.get('meal', '')
  source = request.form.get('source', '')
  other_source = request.form.get('other_source', '')

  text = request.form.get('review', '')
  rating = request.form.get('rating')

  try:
    rating = float(rating)
  except:
    rating = ''

  if not (meal and text and rating and ((source == 'other' and other_source) or (source != 'other' and source))):
    flash('Error submitting review. Verify all required fields are filled.', 'danger')
    return render_template('pages/edit_review.html',
      meal=meal,
      source=source,
      review=text,
      other_source=other_source,
      rating=rating
    )

  if len(meal) > 100 or len(source) > 50:
    flash('There was an error submitting the form.', 'danger')
    return render_template('pages/edit_review.html',
      meal=meal,
      source=source,
      review=text,
      other_source=other_source,
      rating=rating
    )

  if source == 'other':
    source = other_source

  if len(text) > 140:
    shortened_text = text[:137] + '...'
  else:
    shortened_text = text[:140]

  image_url = ''

  if 'image' in request.files:
    image = request.files['image'].read()
    if image:
      res = upload_image(image).json()

      if res['status'] == 200:
        image_url = res['data']['link']

  if review == None:
    review = Review(
      date=datetime.datetime.now(),
      user=request.user
    )

  review.meal = meal
  review.source = source
  review.rating = rating
  review.text = text
  review.shortened_text = shortened_text
  review.image = image_url or review.image

  db.session.add(review)
  db.session.commit()

  return redirect(url_for('views.home'))


@views.route('/reviews/<int:id>/edit', methods=['GET', 'POST'])
def edit_review(id):
  review = Review.query.filter_by(id=id).first()

  if not review:
    return redirect(url_for('views.home'))

  if request.method == 'GET':
    source = review.source
    other_source = ''

    if review.source not in current_app.config.get('RESTAURANTS', []):
      source = 'other'
      other_source = review.source

    return render_template('pages/edit_review.html',
      meal=review.meal,
      source=source,
      review=review.text,
      other_source=other_source,
      rating=review.rating
    )

  return create_or_update_review(review)

@views.route('/reviews/<int:id>')
def show_review(id):
  review = Review.query.filter_by(id=id).first()

  if not review:
    return redirect(url_for('views.home'))

  return render_template('pages/review.html', review=review, user_id=review.user.id)

@views.route('/new', methods=['GET', 'POST'])
def new_review():
  if not request.user:
    return redirect(url_for('views.home'))

  if request.method == 'GET':
    return render_template('pages/edit_review.html')

  
  return create_or_update_review()

  
