from flask import Flask
from flask_bootstrap import Bootstrap
#from . import default_config

def create_app(test_config=None):
    """ application factory function, create and configure the app """
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load default config
        app.config.from_object("yaml_to_json.default_config")
        # load config from file pointed to in environment variable
        # ignore if missing
        app.config.from_envvar("APP_CONFIG", silent=True)
        if not app.config.get('SECRET_KEY', None):
            raise ValueError("No SECRET_KEY set for Flask application")
    else:
        app.config.from_mapping(test_config)

    Bootstrap(app)

    from . import convert
    app.register_blueprint(convert.bp)

    return app
