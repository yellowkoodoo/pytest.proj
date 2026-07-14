from dataclasses import dataclass
from decimal import Decimal

from framework.enums.shop.goods import Goods


@dataclass
class PurchaseItem:
    item: Goods
    number: int
    price: Decimal
