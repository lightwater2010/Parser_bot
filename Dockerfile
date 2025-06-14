# Используем официальный образ Scalingo для Python
FROM scalingo/python:latest

# Устанавливаем системные зависимости для Playwright
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # Основные зависимости для Chromium
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libatspi2.0-0 \
    libdrm2 \
    # Дополнительные зависимости
    libxshmfence1 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libxext6 \
    libxfixes3 \
    libxtst6 \
    # Очистка кеша
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем браузеры Playwright
RUN playwright install chromium

# Копируем исходный код
COPY . .

# Команда запуска (измените под свой проект)
CMD ["python", "bot.py"]