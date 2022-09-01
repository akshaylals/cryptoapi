from importlib import import_module
from flask import Flask

from .config import Config

appsList = (
    'cert',
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    for module_name in appsList:
        module = import_module('apps.{}.routes'.format(module_name))
        print(module.bp)
        app.register_blueprint(module.bp)
    
    return app
