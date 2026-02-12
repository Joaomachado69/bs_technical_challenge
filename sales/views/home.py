from django.template.response import TemplateResponse
from sales.models import Cart
from django.db.models import Sum

__all__ = ["home_view"]
def home_view(request):
    cart_id = request.session.get('cart_id')
    cart = Cart.objects.filter(id=cart_id).first() if cart_id else None
    cart_item_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0 if cart else 0
    
    return TemplateResponse(request, "sales/home.html", {
        "cart_item_count": cart_item_count
    })