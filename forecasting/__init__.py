import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from forecasting.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()


def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)
  app.config['SECRET_KEY'] = 'a2719fe32c7b27d059802dfd728ad86d'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'site.db')

  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)
  mail.init_app(app)

  from forecasting.users.routes import users
  from forecasting.posts.routes import posts
  from forecasting.main.routes import main
  from forecasting.errors.handlers import errors
  app.register_blueprint(users)
  app.register_blueprint(posts)
  app.register_blueprint(main)
  app.register_blueprint(errors)

  return app