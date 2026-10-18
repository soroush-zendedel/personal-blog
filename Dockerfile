FROM python:3.12-slim AS mkdocs-base

WORKDIR /workspace

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM mkdocs-base AS development
EXPOSE 8000
CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000"]

FROM mkdocs-base AS site-builder
RUN mkdocs build --clean

FROM nginx:alpine AS production
COPY --from=site-builder /workspace/site/ /usr/share/nginx/html/
EXPOSE 80
