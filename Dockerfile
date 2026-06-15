
FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    bash \
    ffmpeg \
    git \
    zip \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev \
    pkg-config \
    && pip install --no-cache-dir uv \
    && uv sync --frozen \
    && apt-get remove -y --purge \
       build-essential \
       python3-dev \
       libssl-dev \
       libffi-dev \
       pkg-config \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/app/.venv/bin:$PATH"

CMD ["bash", "start"]