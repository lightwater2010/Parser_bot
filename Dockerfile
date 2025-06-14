FROM ubuntu:22.04  # Используем базовый Ubuntu вместо scalingo/python

# Установка всех системных зависимостей
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
    wget \
    python3.10 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Создаем симлинк для python
RUN ln -s /usr/bin/python3.10 /usr/bin/python

WORKDIR /app
COPY . .

# Установка Python-зависимостей
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium

# Фиктивный web-процесс для Scalingo
CMD ["python", "-m", "http.server", "8080"]
