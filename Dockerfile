FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd -g 1000 appuser && useradd -u 1000 -g appuser -s /bin/bash -m appuser

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    libmagic1 \
    libpcre3 \
    mime-support \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser ./app/. /app

RUN mkdir ./static && chown -R appuser ./static

USER appuser

EXPOSE 8000
