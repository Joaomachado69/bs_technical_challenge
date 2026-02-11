from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from sales.models import Cart, Order, OrderItem
from django.db.models import Sum

__all__ = ["review_cart", "place_order"]

def get_cart(request):
    cart_id = request.session.get('cart_id')
    return Cart.objects.filter(id=cart_id).first() if cart_id else None

def review_cart(request):
    cart = get_cart(request)
    items = cart.items.all() if cart else []
    total = cart.total if cart else 0
    
    cart_item_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0 if cart else 0
    
    return render(request, "sales/review.html", {
        "items": items,
        "total": total,
        "cart_item_count": cart_item_count
    })

@require_POST
def place_order(request):
    
    cart = get_cart(request)
    
    if not cart or not cart.items.exists():
        return redirect('sales:product_list')
    
    order = Order.objects.create(total=cart.total)
    
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        
        product = item.product
        product.stock_qty -= item.quantity
        product.save()
    
    cart.items.all().delete()
    return redirect('sales:home')