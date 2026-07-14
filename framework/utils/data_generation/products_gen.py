import random
from decimal import Decimal

from faker import Faker

from framework.enums.shop.goods import Goods
from framework.models.ui.purchase_item import PurchaseItem

fake = Faker()


class PurchaseGenerator:
    @staticmethod
    def purchase_item(count: int) -> list[PurchaseItem]:
        return [
            PurchaseItem(
                item=PurchaseGenerator._item_available(),
                number=PurchaseGenerator._number(),
                price=Decimal(0),
            )
            for _ in range(count)
        ]

    @staticmethod
    def purchase_item_not_available() -> PurchaseItem:
        return PurchaseItem(
            item=PurchaseGenerator._items_not_available()[0],
            number=PurchaseGenerator._number(),
            price=Decimal(0),
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
            item
            for item in Goods
            if item not in PurchaseGenerator._items_not_available()
        ]

    @staticmethod
    def _item_available():
        return random.choice(PurchaseGenerator._items_available())
