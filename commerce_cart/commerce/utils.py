from decimal import Decimal
from commerce_cart.commerce.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {'quantity': quantity}
        self.save()

    def update(self, product_id, quantity):
        product_id = str(product_id)
        if quantity > 0:
            self.cart[product_id] = {'quantity': quantity}
        else:
            self.remove(product_id)
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            quantity = self.cart[str(product.id)]['quantity']
            total_price = product.price * quantity
            yield {
                'product': product,
                'quantity': quantity,
                'total_price': total_price
            }

    def get_total_price(self):
        return sum(item['total_price'] for item in self)
