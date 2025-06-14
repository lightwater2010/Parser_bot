FROM scalingo/python:latest

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libasound2 libatspi2.0-0 libdrm2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Установка Python-зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Заглушка для Scalingo (требует web-процесс)
CMD ["python", "-m", "http.server", "${PORT:-8080}"]
