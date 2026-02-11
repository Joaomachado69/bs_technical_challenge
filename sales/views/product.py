from django.shortcuts import render, get_object_or_404
from sales.models import Product, Cart, CartItem
from django.db.models import Sum

def product_list(request):
    query = request.GET.get('q', '')
    
    cart_id = request.session.get('cart_id')
    cart = Cart.objects.filter(id=cart_id).first() if cart_id else None
    
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    for product in products:
        if cart:
            product.cart_item = cart.items.filter(product=product).first()
        else:
            product.cart_item = None

    cart_item_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0 if cart else 0

    context = {
        "products": products,
        "query": query,
        "cart_item_count": cart_item_count, 
    }

    if request.headers.get('HX-Request'):
        return render(request, "sales/partials/_product_items.html", context)
    return render(request, "sales/product_list.html", context)

def product_detail_modal(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    cart_id = request.session.get('cart_id')
    cart = Cart.objects.filter(id=cart_id).first() if cart_id else None
    
    cart_item = cart.items.filter(product=product).first() if cart else None
    
    return render(request, "sales/partials/_product_modal.html", {
        "product": product,
        "item": cart_item  
    })