from flask import Flask

def create_app(config='cfr.config.Config'):
  app = Flask(__name__)

  app.config.from_object(config)

  with app.app_context():
    from cfr.views import views
    app.register_blueprint(views)

  return app
