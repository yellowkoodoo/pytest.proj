from dataclasses import dataclass

from framework.models.api.responses.user_response import UserResponse


@dataclass
class LoginResponse:
    token: str
    user: UserResponse
