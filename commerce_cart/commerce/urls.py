from django.urls import path
from commerce_cart.commerce.views import (
    CartView,
    OrderView
)

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('orders/', OrderView.as_view(), name='orders'),
]
