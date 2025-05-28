from django.urls import path
from commerce_cart.commerce.views import AddToCartView, CartView, OrderView

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("add-to-cart/", AddToCartView.as_view(), name="add_to_cart"),
    path("orders/", OrderView.as_view(), name="orders"),
]
