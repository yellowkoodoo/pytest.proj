from faker import Faker

from framework.data.users import User

fake = Faker()


class UserGenerator:
    @staticmethod
    def create_user() -> User:
        return User(
            name=fake.name(), email=fake.unique.email(), password=fake.password()
        )
