from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from commerce_cart.core.models import AbstractBaseModel, DataLookup


class Product(AbstractBaseModel):
    """
    Represents a product available for purchase.
    """
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100
    )

    price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name=_("Price"))

    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"),
        default=1
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name']

    def reduce_stock(self, quantity):
        if quantity > self.quantity:
            raise ValueError(f"Cannot reduce stock below zero for {self.name}")
        self.quantity -= quantity
        self.save()

    def __str__(self) -> str:
        return f"{self.name} (${self.price})"


class Cart(AbstractBaseModel):
    """
    Represents a user's shopping cart.
    Linked to session or user anonymously via session_key.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("User")
    )

    session_key = models.CharField(
        verbose_name=_("Session Key"),
        max_length=100
    )

    class Meta:
        verbose_name = "Shopping Cart"
        verbose_name_plural = "Shopping Carts"

    def __str__(self) -> str:
        return f"{self.id}"


class CartItem(AbstractBaseModel):
    """
    Represents an item added to a shopping cart, including quantity.
    """
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Cart")
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Product")
    )

    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"),
        default=1
    )

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price


class Order(AbstractBaseModel):
    """
    Represents a Users order.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("User")
    )

    session_key = models.CharField(
        verbose_name=_("Session Key"),
        max_length=40, null=True, blank=True, db_index=True)

    code = models.CharField(
        verbose_name=_("Code"),
        max_length=50, unique=True)

    status = models.ForeignKey(
        DataLookup,
        on_delete=models.RESTRICT,
        limit_choices_to={"type": "order_status"},
        related_name="+",
        verbose_name=_("Status")
    )

    total_price = models.DecimalField(
        verbose_name=_("Total Price"),
        max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Order {self.code}"


class OrderItem(AbstractBaseModel):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name=_("Order")
    )

    product_name = models.CharField(
        verbose_name=_("Product Name"),
        max_length=100
    )

    price_at_purchase = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=10, decimal_places=2)

    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        unique_together = ('order', 'product_name')

    def __str__(self) -> str:
        return f"{self.quantity} x {self.product_name} for ${self.price_at_purchase:.2f} each"
