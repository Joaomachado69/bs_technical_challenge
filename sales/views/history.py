from django.shortcuts import render
from sales.models import Order, Cart
from django.db.models import Sum

__all__ = ["order_history"]

def order_history(request):
    
    orders = Order.objects.prefetch_related('items__product').all().order_by('-created_at')
    
    cart_id = request.session.get('cart_id')
    cart = Cart.objects.filter(id=cart_id).first() if cart_id else None
    cart_item_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0 if cart else 0

    context = {
        "orders": orders,
        "cart_item_count": cart_item_count,
    }
    return render(request, "sales/order_history.html", context)