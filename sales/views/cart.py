from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from sales.models import Product, Cart, CartItem
from django.db.models import Sum
from django.contrib import messages 


def get_or_create_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.filter(id=cart_id).first()
        if not cart:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    return cart

@require_POST
def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 0))

    if quantity > product.stock_qty:
        quantity = product.stock_qty
        messages.warning(request, f"Only {product.stock_qty} units available in stock.")
    
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    if quantity <= 0:
        if cart_item:
            cart_item.delete()
            messages.info(request, f"Removed {product.name} from cart.")
        item = None
    else:
        if cart_item:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
            messages.success(request, f"Added {product.name} to cart!")
        item = cart_item

    total_qty = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
    cart_total = cart.total 

    return render(request, "sales/partials/_cart_control_oob.html", {
        'product': product,
        'item': item,
        'cart_item_count': total_qty,
        'cart_total': cart_total,
        'messages': messages.get_messages(request),
    })