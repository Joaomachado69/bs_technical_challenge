from django.shortcuts import render, get_object_or_404 
from sales.models import Product

__all__ = ["product_list","product_detail_modal"]

def product_list(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    context = {
        "products": products,
        "query": query,
    }
    if request.headers.get('HX-Request'):
        return render(request, "sales/partials/_product_items.html", context)
    return render(request, "sales/product_list.html", context)

def product_detail_modal(request ,pk):
    product = get_object_or_404(Product, pk = pk)
    return render (request, "sales/partials/_product_modal.html", {"product": product})
    