from src.main.routes.currency import currency_bp


def register_routes(app):
    app.register_blueprint(currency_bp)

    return app
