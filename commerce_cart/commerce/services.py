from django.db import transaction
from commerce_cart.commerce.enums import ORDER_STATUS_TYPE, OrderStatus
from commerce_cart.commerce.models import Order, OrderItem, Product
from commerce_cart.core.models import DataLookup
from commerce_cart.core.utils import generate_unique_code


class OrderService:
    @staticmethod
    def get_order_status() -> DataLookup:
        try:
            order_status = DataLookup.objects.get(
                type=ORDER_STATUS_TYPE, value=OrderStatus.PENDING.value
            )
            return order_status

        except DataLookup.DoesNotExist:
            # TODO: Add proper custom exception for missed lookup
            raise ValueError("Invalid lookup")

    @staticmethod
    def create_order(session_key, cart):
        with transaction.atomic():
            order = Order.objects.create(
                session_key=session_key,
                code=generate_unique_code(prefix="ORD", unique_identifier=session_key),
                total_price=cart.get_total_price(),
                status=OrderService.get_order_status(),
            )
            for item in cart:
                product: Product = item["product"]
                quantity = item["quantity"]

                OrderItem.objects.create(
                    order=order,
                    product_name=product.name,
                    quantity=quantity,
                    price_at_purchase=product.price,
                )
                product.reduce_stock(quantity)
