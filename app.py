from importlib import import_module
from flask import Flask
from dotenv import load_dotenv
import os
from common.middlewares import log_request

load_dotenv()

BEARER = os.getenv("BEARER")

if BEARER is None:
    raise ValueError("Bearer token is not set in environment variables.")

def create_app():
    
    app = Flask(__name__)

    # Middleware global
    app.before_request(log_request)

     # Registrar blueprints automáticamente
    modules_path = "src.modules"
    modules_dir = os.path.join(os.path.dirname(__file__), "src", "modules")

    for module_name in os.listdir(modules_dir):
        module_path = f"{modules_path}.{module_name}.routes"
        try:
            module = import_module(module_path)
            blueprint = getattr(module, f"{module_name}_bp")
            app.register_blueprint(blueprint, url_prefix=f"/{module_name}")
        except (ModuleNotFoundError, AttributeError):
            continue

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
