# scripts/generate_openapi.py
import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import yaml
import os
import sys
import time

# Добавляем путь к src
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.main import app

def generate_openapi():
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="critical"))
    import threading
    thread = threading.Thread(target=server.run)
    thread.start()
    time.sleep(2)

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    with open("openapi.yaml", "w", encoding="utf-8") as f:
        yaml.dump(openapi_schema, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print("✅ OpenAPI документация успешно сгенерирована в openapi.yaml")

if __name__ == "__main__":
    generate_openapi()