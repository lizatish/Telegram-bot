from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()


app = Flask(__name__)
# app.config.from_object(config_class)
#  TODO: добавить конфиги и фабрику
db.init_app(app)
migrate.init_app(app, db)
with app.app_context():
    db.create_all()

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
