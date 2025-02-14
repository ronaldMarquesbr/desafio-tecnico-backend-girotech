from src.main.routes.currency import currency_bp
from src.main.routes.investor import investor_bp
from src.main.routes.exchange_rate import exchange_rate_bp


def register_routes(app):
    app.register_blueprint(currency_bp)
    app.register_blueprint(investor_bp)
    app.register_blueprint(exchange_rate_bp)

    return app
