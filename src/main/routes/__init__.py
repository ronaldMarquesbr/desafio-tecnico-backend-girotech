from src.main.routes.hello_world import hello_bp


def register_routes(app):
    app.register_blueprint(hello_bp)

    return app
