def create_headers(session: str | None = None) -> dict[str, str]:
    headers = {
        "Content-Type": "application/json",
    }

    if session:
        headers["Authorization"] = f"Bearer {session}"

    return headers
