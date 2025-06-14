FROM scalingo/python:latest

# Установка ВСЕХ необходимых зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxfixes3 \
    libgbm1 \
    libasound2 \
    libatspi2.0-0 \
    libdrm2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium

# Запуск бота
CMD ["python", "bot.py"]
