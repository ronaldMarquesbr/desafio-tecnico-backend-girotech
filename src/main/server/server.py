from flask import Flask
from src.drivers.database import db
from src.main.routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

    db.init_app(app)

    register_routes(app)

    return app
