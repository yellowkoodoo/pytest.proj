import pytest

from framework.core.app import App
from framework.enums.shop.payment_methods import PaymentMethods
from framework.models.ui.purchase_item import PurchaseItem
from framework.utils.data_generation.products_gen import PurchaseGenerator


@pytest.mark.smoke
def test_purchase_credit_card_success(app_logged_in: App):
    items: list[PurchaseItem] = PurchaseGenerator.purchase_item()
    payment: PaymentMethods = PaymentMethods.CreditCard

    app_logged_in.FLOWS.purchase.add_items(items)

    app_logged_in.FLOWS.cart.verify(items)
    app_logged_in.FLOWS.cart.checkout()

    order_id = app_logged_in.FLOWS.checkout.place_order(payment)

    app_logged_in.FLOWS.order.verify_success()
    app_logged_in.FLOWS.order.open(order_id)

    app_logged_in.page.pause()
