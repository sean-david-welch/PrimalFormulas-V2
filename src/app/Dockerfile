FROM python:3.11 AS builder

WORKDIR /app

RUN python -m venv .venv
ENV PATH="./.venv/bin:$PATH"

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y nginx supervisor && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY . .

CMD ["/usr/bin/supervisord"]

EXPOSE 80
