from src.app import db


class Link(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    alias = db.Column(db.String(255), unique=True, nullable=False)
    url = db.Column(db.String(255))
    password = db.Column(db.String(255))
    click_times = db.Column(db.Integer)
    is_phishing = db.Column(db.Boolean)
    user_id = db.Column(db.String(255), db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='links')

    def __init__(self, id, alias, url, user_id):
        self.id = id
        self.alias = alias
        self.url = url
        self.user_id = user_id
        self.click_times = 0
        self.is_phishing = False


class User(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    is_administrator = db.Column(db.Boolean)
    is_blocked = db.Column(db.Boolean)
    token = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean)
    links = db.relationship("Link", back_populates="user", cascade='all, delete-orphan')

    def __init__(self, id, username, email, password, token):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.token = token
        self.is_administrator = False
        self.is_blocked = False
        self.is_verified = False

    def ___json__(self):
        return {
            'id': self.id
        }


class Advertisement(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    expiration_date = db.Column(db.DateTime)

    def __init__(self, id, title, description, image, url, expiration_date):
        self.id = id
        self.title = title
        self.description = description
        self.image = image
        self.url = url
        self.expiration_date = expiration_date
