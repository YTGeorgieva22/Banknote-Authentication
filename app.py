from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from config import Config
from __init__ import create_app
from auth.models import User

app = create_app(Config)

bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run()
