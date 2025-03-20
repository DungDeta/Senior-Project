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

with app.app_context():
    db.create_all()
from src.routes.homepage import homepage
from src.routes.user_management import user_management
from src.routes.link_management import link_management
from src.routes.advertisement_management import advertisement_management
from src.routes.login import login
from src.routes.register import register
from src.routes.redirect_short_link import redirect_short_link
from src.routes.user import user_blueprint
from src.routes.link import link_blueprint
from src.routes.mail import mail_blueprint
from src.routes.advertisement import advertisement_blueprint
from src.routes.social_media import social_media_blueprint
# Đăng ký các blueprint
app.register_blueprint(user_blueprint)
app.register_blueprint(link_blueprint)
app.register_blueprint(mail_blueprint)
app.register_blueprint(advertisement_blueprint)
app.register_blueprint(social_media_blueprint)

if __name__ == '__main__':
    app.run(debug=True)