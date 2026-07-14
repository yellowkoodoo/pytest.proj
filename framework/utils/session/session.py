from pathlib import Path

from framework.models.api.responses.login_response import LoginResponse

ARTIFACTS_DIR = Path("artifacts")
ARTIFACTS_DIR.mkdir(exist_ok=True)

_SESSION_FILE = ARTIFACTS_DIR / "auth-token"


def store_session(login: LoginResponse) -> None:
    _SESSION_FILE.write_text(login.token, encoding="utf-8")


def read_session() -> str:
    return _SESSION_FILE.read_text(encoding="utf-8")


def dispose_session() -> None:
    if _SESSION_FILE.exists():
        _SESSION_FILE.unlink()
