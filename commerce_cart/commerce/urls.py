from django.urls import path
from commerce_cart.commerce.views import (
    CartView,
    #   AddToCartView, RemoveFromCartView,
    # UpdateQuantityView, BuyCartView
)

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    # path(
    #     "add/<int:product_id>/",
    #     AddToCartView.as_view(),
    #     name="add_to_cart"
    # ),
    # path(
    #     "remove/<int:item_id>/",
    #     RemoveFromCartView.as_view(),
    #     name="remove_from_cart"
    # ),
    # path(
    #     "update/<int:item_id>/",
    #     UpdateQuantityView.as_view(),
    #     name="update_quantity"
    # ),
    # path("buy/", BuyCartView.as_view(), name="buy_cart"),
]
