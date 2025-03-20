from src.app import app, db
from src.routes.homepage import homepage
from src.routes.user_management import user_management
from src.routes.link_management import link_management
from src.routes.login import login
from src.routes.register import register
from src.routes.redirect_short_link import redirect_short_link
from src.routes.user import user_blueprint
from src.routes.link import link_blueprint
from src.routes.mail import mail_blueprint
from src.routes.advertisement import advertisement_blueprint
from src.routes.social_media import social_media_blueprint

app.register_blueprint(social_media_blueprint, name='social_media_blueprint')
app.register_blueprint(user_blueprint, name='user_blueprint')
app.register_blueprint(link_blueprint, name='link_blueprint')
app.register_blueprint(mail_blueprint, name='mail_blueprint')
app.register_blueprint(advertisement_blueprint, name='advertisement_blueprint')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0")
