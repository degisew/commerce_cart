from django.test import Client
import pytest
from commerce_cart.commerce.models import Product
from commerce_cart.core.models import DataLookup
from commerce_cart.commerce.services import OrderService
from commerce_cart.commerce.enums import ORDER_STATUS_TYPE, OrderStatus


@pytest.mark.django_db
def test_order_submission_deducts_inventory(client: Client) -> None:
    DataLookup.objects.create(type=ORDER_STATUS_TYPE, value=OrderStatus.PENDING.value)
    product = Product.objects.create(name="Apple", price=10, quantity=5)

    class FakeCart:
        def __iter__(self):
            yield {"product": product, "quantity": 2}

        def get_total_price(self):
            return 20

    session_key = "test123"
    OrderService.create_order(session_key, FakeCart())

    product.refresh_from_db()
    assert product.quantity == 3
