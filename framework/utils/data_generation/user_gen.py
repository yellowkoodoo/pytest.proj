from faker import Faker

from framework.data.users import User

fake = Faker()


class UserGenerator:
    @staticmethod
    def create_user() -> User:
        return User(email=fake.unique.email(), password=fake.password())
