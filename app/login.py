import re

from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from .models import User

def enforce_password_requirements(password):

    return True