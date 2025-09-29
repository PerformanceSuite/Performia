# syntax=docker/dockerfile:1.7
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY services/common /app/services/common
COPY services/melody_bass /app/services/melody_bass

RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r services/melody_bass/requirements.txt

ENTRYPOINT ["python", "-m", "services.melody_bass.main"]
