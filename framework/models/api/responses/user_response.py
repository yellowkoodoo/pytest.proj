from dataclasses import dataclass


@dataclass
class UserResponse:
    id: str
    email: str
    name: str
    role: str
