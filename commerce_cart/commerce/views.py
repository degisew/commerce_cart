from django.views.generic import TemplateView
# from django.http import HttpRequest
# from .models import Cart, CartItem
from commerce_cart.commerce.models import Product, Order, OrderItem
from commerce_cart.commerce.utils import Cart

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages


# def _get_or_create_cart(request: HttpRequest) -> Cart:
#     """
#     Retrieves the cart associated with the current session, or creates a new one.
#     """
#     if not request.session.session_key:
#         request.session.save()
#     session_key = request.session.session_key
#     cart, _ = Cart.objects.get_or_create(session_key=session_key)
#     return cart


class HomeView(TemplateView):
    template_name = "home.html"


# class CartDetailView(TemplateView):
#     template_name = "commerce/cart.html"

#     def get_context_data(self, **kwargs):
#         cart = _get_or_create_cart(self.request)
#         items = cart.items.select_related('product')
#         total = sum(item.get_total_price() for item in items)

#         return {"items": items, "total": total}


class CartView(View):
    def get(self, request):
        cart = Cart(request)

        # Demo: Preload cart with 3 products only once
        if not cart.cart:
            first_three = Product.objects.all()[:3]
            for p in first_three:
                cart.add(p.id, quantity=1)

        return render(request, 'commerce/cart.html', {
            'cart_items': list(cart),
            'total': cart.get_total_price()
        })

    def post(self, request):
        cart = Cart(request)
        errors = []

        for key, value in request.POST.items():
            if key.startswith("quantity_"):
                product_id = key.split("_")[1]
                try:
                    product = Product.objects.get(id=product_id)
                    requested_qty = int(value)
                except (Product.DoesNotExist, ValueError):
                    continue

                if requested_qty > product.quantity:
                    if product.quantity == 0:
                        errors.append(f"Sorry, {product.name} is out of stock.")
                    else:
                        errors.append(f"Sorry, only {product.quantity} {product.name} left.")
                else:
                    cart.update(product_id, requested_qty)

        if errors:
            for err in errors:
                messages.error(request, err)
            return redirect('cart')

        # All good → Create Order
        order = Order.objects.create()
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )
            # Deduct quantity
            item['product'].quantity -= item['quantity']
            item['product'].save()

        cart.clear()
        messages.success(request, "Your order has been placed successfully.")
        return redirect('cart')
