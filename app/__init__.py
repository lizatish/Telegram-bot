import telebot
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# app.config.from_object(config_class)
#  TODO: добавить фабрику
# migrate.init_app(app, db)
with app.app_context():
    db.create_all()
bot = telebot.TeleBot(token=app.config['TELEGRAM_TOKEN'])

# def create_app(config_class=Config):
#     app = Flask(__name__)
#     app.config.from_object(config_class)
#
#     db.init_app(app)
#     migrate.init_app(app, db)
#     with app.app_context():
#         db.create_all()
#     return app


from app import routes, models
