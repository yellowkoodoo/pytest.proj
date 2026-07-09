from framework.models.user import User


class Users:
    ADMIN = User(
        email="admin@shop.com",
        password="admin999",
    )

    ALICE = User(
        email="alice@example.com",
        password="pass123",
    )
