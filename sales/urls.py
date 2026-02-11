from django.urls import path
import sales.views as views

app_name = "sales"

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/modal/', views.product_detail_modal, name='product_detail_modal'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),

]