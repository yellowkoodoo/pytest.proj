# README.md

## Reporting used:
TBD

## Installation:

bash:
1) setup .venv: `python -m venv .venv`
2) acivate .venv: `.venv/Scripts/activate`
3) run `pip install -e ".[dev]"`
4) run `python -m playwright install` to install browsers (might need an increased timeout: `PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT=120000 npx playwright install`)

## Run tests locally

./scripts/test-qa.sh -m debug