
FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    curl \
    ffmpeg \
    git \
    zip \
    gcc \
    g++ \
    musl-dev \
    build-essential \
    python3-dev \
    libffi-dev \
    libssl-dev \
    pkg-config \
    && pip install --no-cache-dir uv \
    && pip install -U aiogram python-telegram-bot \
    && uv sync --frozen \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/app/.venv/bin:$PATH"

CMD ["bash", "start"]