# README.md

## Installation:

bash:
1) setup .venv: `python -m venv .venv`
2) acivate .venv: `.venv/Scripts/activate`
3) run `pip install -e ".[dev]"`
4) run `playwright install` (might need an increased timeout: `PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT=120000 npx playwright install`)