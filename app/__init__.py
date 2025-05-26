from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = None
login_manager = LoginManager()
db = SQLAlchemy()

def create_app():
    global app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'


    from app import routes, models, events
    with app.app_context():
        db.create_all()

    return app