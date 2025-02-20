import os
import toml
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.models import models

app = Flask(__name__)
config_path = os.path.join(os.path.dirname(__file__), 'config.toml')
config = toml.load(config_path)
app.config.update(config['default'])
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://root:{config['mysql']['MYSQL_PASSWORD']}@localhost:{config['mysql']['MYSQL_PORT']}/{config['mysql']['MYSQL_DATABASE']}"

STATIC_DIR = os.path.abspath('src/static')
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()