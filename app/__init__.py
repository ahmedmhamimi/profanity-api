from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    
    from .routes import api
    app.register_blueprint(api)

    return app
