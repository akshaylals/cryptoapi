from importlib import import_module
from flask import Flask

from .config import Config
from .database import db

appsList = (
    'auth',
    'cert',
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    for module_name in appsList:
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.bp)
    
    return app
