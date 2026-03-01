FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir .

CMD ["mcp-suno", "--transport", "http", "--port", "8000"]
