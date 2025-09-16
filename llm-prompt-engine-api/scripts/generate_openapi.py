# scripts/generate_openapi.py
import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import yaml
import os
import sys

# ⚠️ КРИТИЧНО: Добавляем путь к src — без этого импорт сломается!
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.main import app

def generate_openapi():
    # ⚠️ ВАЖНО: Используем uvicorn.run() напрямую — БЕЗ потоков!
    # И используем host="0.0.0.0" — чтобы сервер был доступен изнутри контейнера
    config = uvicorn.Config(
        app,
        host="0.0.0.0",   # 🟢 Разрешаем входящие соединения
        port=8000,
        log_level="critical",
        reload=False      # 🟢 Не нужно перезагружать в CI
    )
    server = uvicorn.Server(config)

    # ⚠️ ВАЖНО: Запускаем сервер как блокирующий процесс — так он гарантированно будет готов
    server.run()

    # После того как сервер запущен — получаем OpenAPI схему
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
