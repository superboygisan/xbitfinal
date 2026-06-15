FROM python:3.11-slim

WORKDIR /app

# 1. Pehle saare system tools install karein
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

# 2. Files copy karein
COPY . /app/

# 3. Pip aur UV ko ek baar clear setup karein
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir uv

# 4. Ab uv sync chalayein bina frozen ke, taaki pyproject.toml se KurvaGram directly install ho jaye
RUN uv sync --no-frozen

# 5. Virtual environment ka path set karein
ENV PATH="/app/.venv/bin:$PATH"

CMD ["bash", "start"]
