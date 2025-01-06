from importlib import import_module
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import uvicorn
from common.middlewares import LogRequestMiddleware

load_dotenv()

BEARER = os.getenv("BEARER")

if BEARER is None:
    raise ValueError("Bearer token is not set in environment variables.")

app = FastAPI()

# Middleware global
app.add_middleware(LogRequestMiddleware)


# Registrar routers automáticamente desde los módulos
modules_path = "src.modules"
modules_dir = os.path.join(os.path.dirname(__file__), "src", "modules")

for module_name in os.listdir(modules_dir):
    module_dir = os.path.join(modules_dir, module_name)
    if os.path.isdir(module_dir) and os.path.exists(os.path.join(module_dir, "routes.py")):
        module_path = f"{modules_path}.{module_name}.routes"
        try:
            module = import_module(module_path)
            router = getattr(module, f"{module_name}_router")
            app.include_router(router, prefix=f"/{module_name}")
        except (ModuleNotFoundError, AttributeError) as e:
            print(f"Skipping module {module_name}: {e}")

# Ejecutar la app en local
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
