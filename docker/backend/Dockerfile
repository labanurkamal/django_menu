FROM python:3.10-slim

USER root

WORKDIR /opt/app/

ENV PYTHONDONTWRITECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

COPY /backend/requirements.txt requirements.txt

RUN mkdir -p /opt/app/static/ \
    && mkdir -p /opt/app/media/ \
    && mkdir -p /opt/app/staticfiles/ \
    && pip install --upgrade pip --no-cache-dir \
    && pip install --no-cache-dir -r requirements.txt

COPY docker/backend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY backend/ .

ENTRYPOINT ["/entrypoint.sh"]