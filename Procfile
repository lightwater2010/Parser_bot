web: python -m http.server $PORT
worker: sh -c "export PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright && mkdir -p $PLAYWRIGHT_BROWSERS_PATH && if ! command -v playwright >/dev/null 2>&1; then pip install playwright==1.40.0 && playwright install --with-deps chromium; fi && python bot.py"
