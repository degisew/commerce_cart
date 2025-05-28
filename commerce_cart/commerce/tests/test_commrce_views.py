import pytest
from django.test import Client
from django.urls import reverse
from commerce_cart.commerce.enums import ORDER_STATUS_TYPE, OrderStatus
from commerce_cart.commerce.models import Order, Product, OrderItem, DataLookup


@pytest.mark.django_db
def test_cart_view_get(client: Client) -> None:
    Product.objects.bulk_create(
        [
            Product(name="Apple", quantity=5, price=1.0),
            Product(name="Banana", quantity=3, price=1.5),
            Product(name="Orange", quantity=10, price=2.0),
        ]
    )
    response = client.get(reverse("cart"))
    assert response.status_code == 200
    assert b"Apple" in response.content


@pytest.mark.django_db
def test_orders_listed_by_session(client):
    session = client.session
    session.save()
    session_key = session.session_key

    status = DataLookup.objects.create(
        type=ORDER_STATUS_TYPE,
        value=OrderStatus.PENDING.value,
    )

    order = Order.objects.create(
        session_key=session_key, code="ORD12345", total_price=100, status=status
    )
    OrderItem.objects.create(
        order=order, product_name="Test Product", quantity=2, price_at_purchase=50
    )

    # assuming 'orders' is your URL name
    response = client.get(reverse("orders"))

    assert response.status_code == 200
    assert "Test Product" in response.content.decode()
    assert order in response.context["items"]
