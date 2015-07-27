# config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'BAD-SECRET-KEY'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
CSRF_ENABLED = True

# MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'jiaofcards@gmail.com')
# MAIL_PASSWORD = 'weishengjian'
# MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '"Learn Chinese" <jiaoofcards@gmail.com>')
# MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
# MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
# MAIL_USE_SSL = False
# MAIL_USE_TLS = True

UPLOAD_FOLDER = basedir + "/uploads/"

USER_APP_NAME = "ReadMate" ## change this
