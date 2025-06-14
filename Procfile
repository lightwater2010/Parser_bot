web: python -m http.server $PORT
worker: sh -c "
  mkdir -p ~/.cache/ms-playwright/chromium-1169 &&
  wget https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1169/chrome-linux.zip &&
  unzip chrome-linux.zip -d ~/.cache/ms-playwright/chromium-1169/ &&
  PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 pip install playwright &&
  python bot.py"
