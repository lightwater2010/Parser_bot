FROM ubuntu:22.04

# 1. Установка всех системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 \
    libxfixes3 libgbm1 libasound2 libatspi2.0-0 libdrm2 \
    wget python3.10 python3-pip xvfb \
    && rm -rf /var/lib/apt/lists/*

# 2. Настройка Python
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# 3. Установка Playwright и браузеров
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium

# 4. Копирование кода
COPY . .

# 5. Запуск и worker, и web в одном контейнере
CMD sh -c "python -m http.server 8080 & python bot.py"
