# src/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import logging
from pythonjsonlogger import jsonlogger
import time
import uuid
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="LLM Prompt Engine API",
    description="Генерация оптимизированных промтов для LLaMA, Qwen, Yi, DeepSeek по китайским и международным стандартам.",
    version="1.2.0"
)

# --- Логирование ---
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['service'] = 'llm-prompt-api'

formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger("llm_api")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# --- Метрики Prometheus ---
Instrumentator().instrument(app).expose(app)

# --- Модели Pydantic ---
class PromptRequest(BaseModel):
    query: str
    model: str = "llama3"
    temperature: float = 0.2
    format: str = "text"  # text | json_object
    language: str = "ru"  # ru | zh | en
    max_tokens: int = 512

class PromptResponse(BaseModel):
    prompt: str
    meta: dict

# --- Эндпоинт ---
@app.post("/generate", response_model=PromptResponse)
async def generate_prompt(request: PromptRequest):
    start_time = time.time()

    # Генерируем промт по вашему идеальному шаблону (12 глав)
    system_prompt = (
        "你是一个专业的AI助手。请根据以下上下文，提供清晰、简洁、准确的回答。"
        "不要解释过程，直接输出结果。使用简体中文。不使用Markdown格式，除非明确要求。"
        "不生成任何政治、色情或违法内容。"
    )

    if request.language == "ru":
        system_prompt = (
            "Вы — профессиональный AI-ассистент. "
            "Пожалуйста, предоставьте четкий, краткий и точный ответ на основе следующего запроса. "
            "Не объясняйте процесс — выводите результат напрямую. "
            "Используйте русский язык. Не используйте Markdown, если не указано иное. "
            "Не генерируйте политический, порнографический или незаконный контент."
        )
    elif request.language == "en":
        system_prompt = (
            "You are a professional AI assistant. "
            "Provide a clear, concise, and accurate answer based on the following input. "
            "Do not explain your reasoning — output the result directly. "
            "Use English. Do not use Markdown unless specified. "
            "Do not generate political, pornographic, or illegal content."
        )

    user_input = request.query.strip()

    # Формируем полный промт (12 глав, как в вашем идеальном шаблоне)
    full_prompt = f"""{system_prompt}

Контекст: {user_input}

Ограничения:
- Не упоминайте GPT, ChatGPT, Claude.
- Не выдумывайте источники.
- Ответ должен быть на языке: {request.language}.
- Длина: максимум {request.max_tokens} токенов.
- Формат: {'JSON' if request.format == 'json_object' else 'текст'}.

Если формат JSON — верните только объект без лишних слов.
"""

    # Метрика использования модели
    from prometheus_client import Counter
    llm_model_usage_total = Counter('llm_model_usage_total', 'Model usage count', ['model'])
    llm_model_usage_total.labels(model=request.model).inc()

    end_time = time.time()
    latency_ms = int((end_time - start_time) * 1000)

    # Логируем
    logger.info(
        "Prompt generated",
        extra={
            "user_input": user_input,
            "model": request.model,
            "language": request.language,
            "format": request.format,
            "tokens_input": len(user_input.split()),
            "latency_ms": latency_ms,
            "trace_id": str(uuid.uuid4())
        }
    )

    return {
        "prompt": full_prompt,
        "meta": {
            "model_used": request.model,
            "tokens_input": len(user_input.split()),
            "tokens_output": len(full_prompt.split()),
            "language": request.language,
            "format": request.format,
            "latency_ms": latency_ms,
            "trace_id": str(uuid.uuid4())
        }
    }