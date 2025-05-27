from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model.
    """
    list_display = ("name", "price", "quantity")
    exclude = ("deleted_at",)
    search_fields = ("name",)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    exclude = ("deleted_at",)
    readonly_fields = ('product', 'quantity')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Admin configuration for Cart model.
    """
    list_display = ("id", "session_key", "created_at")
    exclude = ("deleted_at",)
    inlines = [CartItemInline]
    search_fields = ("session_key",)
    readonly_fields = ("created_at",)
    ordering = ['-created_at']


# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     """
#     Admin configuration for CartItem model.
#     """
#     list_display = ("product", "cart", "quantity", "created_at")
#     exclude = ("deleted_at",)
#     search_fields = ("product__name", "cart__session_key")
#     list_filter = ("created_at",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    exclude = ("deleted_at",)
    readonly_fields = ('product_name', 'quantity', 'price_at_purchase')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'total_price')
    exclude = ("deleted_at",)
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'total_price')
    ordering = ['-created_at']
