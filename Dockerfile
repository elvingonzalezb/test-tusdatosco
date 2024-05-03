# Etapa 1: Construir la aplicación
FROM python:3.9-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Etapa 2: Crear la imagen final
FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /app .

RUN pip install fastAPI

EXPOSE 8000

CMD ["python", "src/app.py"]
