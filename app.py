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

# Ruta base para los módulos en términos del espacio de nombres de Python
modules_base_path = "src.modules"

# Directorio base relativo desde app.py
modules_dir = "src/modules"

for module_name in os.listdir(modules_dir):
    module_path = os.path.join(modules_dir, module_name)
    # Verificar si es un directorio y contiene `routes.py`
    if os.path.isdir(module_path) and os.path.exists(os.path.join(module_path, "routes.py")):
        module_import_path = f"{modules_base_path}.{module_name}.routes"
        try:
            module = import_module(module_import_path)
            router = getattr(module, f"{module_name}_router", None)
            app.include_router(router, prefix=f"/{module_name}")
        except (ModuleNotFoundError) as e:
            print(f"Skipping module {module_name}: {e}")
print("APP ROUTES:")
for route in app.routes:
    print(f"Path: {route.path}, Methods: {route.methods}")

# Ejecutar la app en local
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True)
