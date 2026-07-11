import random

from faker import Faker

from framework.enums.shop.goods import Goods
from framework.models.ui.purchase_item import PurchaseItem

fake = Faker()


class UserGenerator:
    @staticmethod
    def purchase_item() -> PurchaseItem:
        return PurchaseItem(
            item=UserGenerator._item_available(), number=UserGenerator._number()
        )

    @staticmethod
    def purchase_item_not_available() -> PurchaseItem:
        return PurchaseItem(
            item=UserGenerator._items_not_available()[0], number=UserGenerator._number()
        )

    @staticmethod
    def _number():
        return fake.random_int(1, 3)

    @staticmethod
    def _item():
        return random.choice(list(Goods))

    @staticmethod
    def _items_not_available():
        return [Goods.DeskLamp]

    @staticmethod
    def _items_available():
        return [
            item for item in Goods if item not in UserGenerator._items_not_available()
        ]

    @staticmethod
    def _item_available():
        return random.choice(UserGenerator._items_available())
