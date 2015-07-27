from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)

from app import routes, models
from flask_user import SQLAlchemyAdapter, UserManager

db_adapter = SQLAlchemyAdapter(db, models.User)
user_manager = UserManager(db_adapter, app)