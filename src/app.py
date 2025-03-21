import os

import redis
import toml
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

STATIC_DIR = os.path.abspath('src/static')
config_path = os.path.join(os.path.dirname(__file__), 'config.toml')
config = toml.load(config_path)
app.config.update(config['default'])
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql://root:{config['mysql']['MYSQL_PASSWORD']}@localhost:{config['mysql']['MYSQL_PORT']}/{config['mysql']['MYSQL_DATABASE']}"

app.config['MAIL_SERVER'] = config['mail']['MAIL_SERVER']
app.config['MAIL_PORT'] = config['mail']['MAIL_PORT']
app.config['MAIL_USE_TLS'] = config['mail']['MAIL_USE_TLS']
app.config['MAIL_USE_SSL'] = config['mail']['MAIL_USE_SSL']
app.config['MAIL_USERNAME'] = config['mail']['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = config['mail']['MAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = config['mail']['MAIL_USERNAME']
app.config['SECRET_KEY'] = config['default']['SECRET_KEY']
db = SQLAlchemy()
bcrypt = Bcrypt(app)
mail = Mail(app)

redis_client = redis.StrictRedis(host='localhost', port=config['redis']['REDIS_PORT'], decode_responses=True)

# Initialize SQLAlchemy with the app
db.init_app(app)
