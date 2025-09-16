# 🚀 LLM Prompt Engine API

> **Генерация оптимизированных промтов для LLaMA, Qwen, Yi, DeepSeek**  
> По лучшим практикам из Hugging Face, LLaMA-Factory, CSDN, ModelScope

[![OpenAPI Docs](https://img.shields.io/badge/OpenAPI-Docs-blue?logo=swagger)](https://otbedy-cyber.github.io/llm-prompt-engine-api/)
[![CI/CD](https://img.shields.io/github/actions/workflow/status/otbedy-cyber/llm-prompt-engine-api/update-openapi.yml?label=CI&logo=github)](https://github.com/otbedy-cyber/llm-prompt-engine-api/actions)
[![Release](https://img.shields.io/github/release/otbedy-cyber/llm-prompt-engine-api/all.svg?label=Release&logo=github)](https://github.com/otbedy-cyber/llm-prompt-engine-api/releases/tag/v1.0.0)

## 🔧 Технологии

- **FastAPI** — асинхронный Python-фреймворк
- **Prometheus + Grafana + Loki** — мониторинг и логи
- **GitHub Actions** — автоматическая генерация документации
- **Swagger UI** — интерактивная документация
- **Docker + Docker Compose** — локальное развертывание
- **LLaMA, Qwen, Yi, DeepSeek** — поддержка китайских моделей

## 🌐 Документация

👉 **Интерактивный Swagger UI**:  
[https://otbedy-cyber.github.io/llm-prompt-engine-api/](https://otbedy-cyber.github.io/llm-prompt-engine-api/)

> 🔄 Автоматически обновляется при каждом пуше в `main`

## 📦 Скачать полный шаблон (ZIP)

📥 **Скачать готовый проект (все файлы, настроенные под вас):**  
[⬇️ Скачать v1.0.0 ZIP](https://github.com/otbedy-cyber/llm-prompt-engine-api/releases/download/v1.0.0/llm-prompt-engine-api_otbedy-cyber.zip)

## 🛠️ Локальный запуск

```bash
# Запустить API
uvicorn src.main:app --reload

# Запустить весь стек (Prometheus/Grafana/Loki)
docker-compose up --build

Откройте:

API: http://localhost:8000/docs
Prometheus: http://localhost:9090
Grafana: http://localhost:3000 (логин: admin/admin)
Loki: http://localhost:3100
📚 Источники
Hugging Face: Chinese-LLaMA-Alpaca
LLaMA-Factory на GitHub
CSDN: 10个高阶LLaMA提示词模板
ModelScope: Qwen-Chat
© 2025 — Сделано с ❤️ для AI-инженеров
