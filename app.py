from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    #Blueprints
    from main.routes import main_bp
    from auth.routes import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app