import re
from re import Pattern


class Regex:
    @staticmethod
    def exact(text: str) -> Pattern[str]:
        return re.compile(f"^{re.escape(text)}$")
