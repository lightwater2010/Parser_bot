FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Загружаем браузеры Playwright (Chromium, Firefox, WebKit)
RUN playwright install --with-deps chromium

# Открываем порт (если ты используешь webhook, иначе можно не нужно)
EXPOSE 8000

# Запускаем бота
CMD ["python", "bot.py"]