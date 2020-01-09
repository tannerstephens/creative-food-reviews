from flask import Flask
from flask_migrate import Migrate

def create_app(config='cfr.config.Config'):
  app = Flask(__name__)
  app.config.from_object(config)

  with app.app_context():
    from cfr.views import views
    app.register_blueprint(views)

    from cfr.api import api
    app.register_blueprint(api)

    from cfr.models import db
    Migrate(app, db)

  return app
