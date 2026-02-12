from django.test import TestCase, Client
from django.urls import reverse
from sales.models import Product, Cart, CartItem

class SalesViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.product = Product.objects.create(
            name="Test Product",
            sku="TEST-SKU-001",
            price=100.00,
            stock_qty=5
        )

    def test_product_list_view(self):
        url = reverse('sales:product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/product_list.html")
        self.assertContains(response, self.product.name)

    def test_product_detail_modal_view(self):
        url = reverse('sales:product_detail_modal', args=[self.product.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/partials/_product_modal.html")
        self.assertContains(response, self.product.name)
        self.assertContains(response, "5 units")

    def test_update_cart_add_logic(self):
        url = reverse('sales:update_cart', args=[self.product.id])
        response = self.client.post(url, {'quantity': 2}, HTTP_HX_REQUEST='true')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertContains(response, "2")
        self.assertContains(response, "item_count_badge") 

    def test_update_cart_stock_limit(self):
        """Requirement: Force quantity to max stock if exceeded."""
        url = reverse('sales:update_cart', args=[self.product.id])
        response = self.client.post(url, {'quantity': 10}, HTTP_HX_REQUEST='true')
        
        cart_item = CartItem.objects.get(product=self.product)
        self.assertEqual(cart_item.quantity, 5) 
        self.assertContains(response, "5")

    def test_update_cart_removal_logic(self):
        """Requirement: Remove item from cart if quantity is 0."""
        url = reverse('sales:update_cart', args=[self.product.id])
        
        self.client.post(url, {'quantity': 1}, HTTP_HX_REQUEST='true')
        
        response = self.client.post(url, {'quantity': 0}, HTTP_HX_REQUEST='true')
        
        self.assertEqual(CartItem.objects.count(), 0)
        self.assertContains(response, "Add to cart") 

    def test_order_history_view(self):
        """Test if the history page lists past orders."""
        from sales.models import Order
        order = Order.objects.create(total=500.00)
        
        url = reverse('sales:order_history')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/order_history.html")
        self.assertContains(response, f"#{order.id}")
        self.assertContains(response, "500.00")