from flask import Flask
from antipatterns.routes import antipatterns_bp
from dotenv import load_dotenv
import os
from common.middlewares import log_request

load_dotenv()

BEARER = os.getenv("BEARER")

if BEARER is None:
    raise ValueError("Bearer token is not set in environment variables.")

def create_app():
    
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Middleware global
    app.before_request(log_request)

    # Registrar los blueprints
    app.register_blueprint(antipatterns_bp, url_prefix="/antipatterns")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
