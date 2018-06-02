from flask import Flask

def create_app():
    app = Flask(__name__.split('.')[0])

    register_blueprint(app)

    return app

def register_blueprint(app):
    from . import base, line

    app.register_blueprint(base.blueprint)
    app.register_blueprint(line.blueprint)
