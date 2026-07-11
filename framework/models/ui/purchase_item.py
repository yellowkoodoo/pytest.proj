from dataclasses import dataclass

from framework.enums.shop.goods import Goods


@dataclass
class PurchaseItem:
    item: Goods
    number: int
