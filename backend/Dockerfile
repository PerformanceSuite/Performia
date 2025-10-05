FROM python:3.11-slim AS base

WORKDIR /app

# Install system dependencies for audio processing and Docling
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpoppler-cpp-dev \
    libsndfile1 \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Docling first (large dependency ~2-3GB)
RUN pip install --no-cache-dir docling==2.55.1

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/rag_storage/chromadb /app/output /app/tmp/final

# Add health check endpoint script
RUN echo '#!/usr/bin/env python3\nfrom fastapi import FastAPI\napp = FastAPI()\n@app.get("/health")\ndef health(): return {"status": "healthy"}' > /tmp/health.py

# Expose port
EXPOSE 8000

# Default command - can be overridden
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
