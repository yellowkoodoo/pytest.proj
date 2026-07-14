from playwright.sync_api import APIRequestContext

from framework.data.users import User
from framework.models.api.responses.login_response import LoginResponse
from framework.utils.session.request import create_headers
from framework.utils.session.session import (
    dispose_session,
    read_session,
    store_session,
)


class AuthApi:
    def __init__(self, request: APIRequestContext):
        self.request = request

    def login(self, user: User) -> LoginResponse:
        response = self.request.post(
            "/auth/login",
            data=user.__dict__,
            headers={
                "Content-Type": "application/json",
            },
        )

        if not response.ok:
            raise RuntimeError(f"Login failed: {response.status} {response.text()}")

        body = response.json()
        login_response = LoginResponse(token=body["token"], user=body["user"])

        store_session(login_response)

        return login_response

    def logout(self, user: User) -> None:
        response = self.request.post(
            "/auth/logout",
            data=user.__dict__,
            headers=create_headers(read_session()),
        )

        dispose_session()

        if not response.ok:
            raise RuntimeError(f"Logout failed: {response.status} {response.text()}")
