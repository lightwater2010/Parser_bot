web: python -m http.server $PORT
worker: sh -c "apt-get update && apt-get install -y --no-install-recommends libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libxfixes3 libgbm1 libasound2 libatspi2.0-0 libdrm2 && playwright install chromium && python bot.py"
