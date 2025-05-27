import pytest
from commerce_cart.commerce.models import Product


@pytest.mark.django_db
def test_product_creation():
    product = Product.objects.create(name="Potatoes", quantity=10, price=2.5)
    assert product.name == "Potatoes"
    assert product.quantity == 10
    assert float(product.price) == 2.5
