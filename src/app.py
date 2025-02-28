import os
import toml
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import redis

app = Flask(__name__)
config_path = os.path.join(os.path.dirname(__file__), 'config.toml')
config = toml.load(config_path)
app.config.update(config['default'])
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://root:{config['mysql']['MYSQL_PASSWORD']}@localhost:{config['mysql']['MYSQL_PORT']}/{config['mysql']['MYSQL_DATABASE']}"

app.config['MAIL_SERVER'] = config['mail']['MAIL_SERVER']
app.config['MAIL_PORT'] = config['mail']['MAIL_PORT']
app.config['MAIL_USE_TLS'] = config['mail']['MAIL_USE_TLS']
app.config['MAIL_USERNAME'] = config['mail']['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = config['mail']['MAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = config['mail']['MAIL_USERNAME']

STATIC_DIR = os.path.abspath('src/static')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

redis_client = redis.StrictRedis(host='localhost', port=config['redis']['REDIS_PORT'], decode_responses=True)

with app.app_context():
    db.create_all()

# Import and register routes
from src.routes import register, login

if __name__ == '__main__':
    app.run()