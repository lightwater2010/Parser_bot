FROM scalingo/python:latest as base

# Установка системных зависимостей для Playwright
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libasound2 libatspi2.0-0 libdrm2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium

# Копирование кода
COPY . .

# ----------------------------
# Этап для web-процесса
FROM base as web
CMD ["python", "-m", "http.server", "$PORT"]  # Или ваш web-сервер

# ----------------------------
# Этап для worker-процесса
FROM base as worker
CMD ["python", "bot.py"]  # Ваш фоновый процесс
