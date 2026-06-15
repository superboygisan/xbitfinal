FROM python:3.11-slim

WORKDIR /app

# System tools install karein
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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

# UV install karein aur dependencies sync karein
RUN pip install --no-cache-dir uv
RUN uv sync --no-frozen

ENV PATH="/app/.venv/bin:$PATH"

CMD ["bash", "start"]
