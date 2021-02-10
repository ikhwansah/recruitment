import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config
from flask_pymongo import PyMongo
import hmac, hashlib

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config.from_object(config[os.getenv('FLASK_CONFIG') or 'default'])
config[os.getenv('FLASK_CONFIG') or 'default'].init_app(app)

db = SQLAlchemy(app)
Migrate(app,db)

mongo = PyMongo(app)
Migrate(app,mongo)

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view= 'access.login'

from app.main.views import core
from app.auth.views import access

app.register_blueprint(core)
app.register_blueprint(access)

def hmac_sha256(key, msg):
    hash_obj = hmac.new(key=key, msg=msg, digestmod=hashlib.sha256)
    return hash_obj.hexdigest()
