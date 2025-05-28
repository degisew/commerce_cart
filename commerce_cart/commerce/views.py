from typing import Any
from django.views import View
from django.contrib import messages
from django.views.generic import TemplateView
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from commerce_cart.commerce.models import Order, Product
from commerce_cart.commerce.services import OrderService
from commerce_cart.commerce.utils import CartMixin


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context


class CartView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        cart = CartMixin(request)

        # Preload cart with 3 products
        if not cart.cart:
            first_three = Product.objects.all()[:3]
            for p in first_three:
                cart.add(p.id, quantity=1)

        return render(
            request,
            "commerce/cart.html",
            {"cart_items": list(cart), "total": cart.get_total_price()},
        )

    def post(self, request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        cart = CartMixin(request)
        errors = []
        for key, value in request.POST.items():
            if key.startswith("quantity_"):
                product_id = key.split("_")[1]
                try:
                    product = Product.objects.get(id=product_id)
                    requested_qty = int(value)
                except (Product.DoesNotExist, ValueError):
                    continue

                cart.update(product_id, requested_qty)

                if requested_qty > product.quantity:
                    if product.quantity == 0:
                        errors.append(f"Sorry, {product.name} is out of stock.")
                    else:
                        errors.append(
                            f"Sorry, only {product.quantity} {product.name} left."
                        )

        if errors:
            for err in errors:
                messages.error(request, err)
        else:
            OrderService.create_order(
                session_key=request.session.session_key, cart=cart
            )
            messages.success(request, "Your order has been placed successfully.")
            cart.clear()

        return redirect("cart")


class AddToCartView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        cart = CartMixin(request)
        product_id = request.POST.get("product_id")
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            try:
                product = Product.objects.get(id=product_id)
                cart.add(product.id, quantity=1)
                return JsonResponse(
                    {
                        "success": True,
                        "message": f"{product.name} added to cart.",
                        "product_name": product.name,
                    }
                )
            except Product.DoesNotExist:
                return JsonResponse({"success": False, "message": "Product not found."})
            except Exception:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Something went wrong. Please try again.",
                    }
                )
        else:
            return JsonResponse({"success": False, "message": "Invalid request."})


class OrderView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        session_key = request.session.session_key
        items = Order.objects.filter(session_key=session_key)
        return render(request, "commerce/orders.html", {"items": items})
