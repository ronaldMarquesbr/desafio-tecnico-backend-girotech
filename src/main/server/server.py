from flask import Flask
from src.drivers.database import db
from src.main.routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

    db.init_app(app)

    register_routes(app)

    with app.app_context():
        db.create_all()

    return app


def create_app_test():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///:memory:'

    db.init_app(app)
    register_routes(app)

    with app.app_context():
        db.create_all()

    return app
