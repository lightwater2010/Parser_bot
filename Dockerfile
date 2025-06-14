FROM scalingo/python:latest

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libasound2 libatspi2.0-0 libdrm2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium

# Фикс для Scalingo - "фейковый" HTTP-сервер + ваш worker
CMD sh -c "python -m http.server 8080 & python bot.py"
