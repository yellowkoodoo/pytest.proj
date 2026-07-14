from framework.models.ui.user import User


class Users:
    ADMIN = User(
        name="Admin",
        email="admin@shop.com",
        password="admin999",
    )

    ALICE = User(
        name="Alice",
        email="alice@example.com",
        password="pass123",
    )
