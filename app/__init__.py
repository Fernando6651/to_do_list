from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
from app.models import User
import os
from flask_mail import Mail

mail = Mail()
mysql = MySQL()
login_manager = LoginManager()

def create_app():
    # Define o caminho para o diretório templates
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))

    app.config.from_object('config')

    mysql.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_user_by_id(user_id)


    from app.routes import main
    app.register_blueprint(main)

    return app
