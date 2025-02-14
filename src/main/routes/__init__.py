from src.main.routes.currency import currency_bp
from src.main.routes.investor import investor_bp


def register_routes(app):
    app.register_blueprint(currency_bp)
    app.register_blueprint(investor_bp)

    return app
