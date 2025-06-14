web: python -m http.server $PORT  # Фиктивный web-процесс

worker: |
  sh -c "
  echo 'Устанавливаем системные зависимости...' &&
  apt-get update &&
  apt-get install -y --no-install-recommends \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 \
    libxfixes3 libgbm1 libasound2 libatspi2.0-0 libdrm2 &&
  echo 'Устанавливаем Playwright...' &&
  playwright install chromium &&
  echo 'Запускаем бота...' &&
  python bot.py
  "