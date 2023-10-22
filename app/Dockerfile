FROM python:3.11 AS builder

WORKDIR /app

RUN python -m venv .venv
ENV PATH="./.venv/bin:$PATH"

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

FROM python:3.11

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY . .

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

