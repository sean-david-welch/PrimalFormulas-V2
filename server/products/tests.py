from django.test import TestCase

from products.models import Products


class ProductViewTest(TestCase):
    def setupProduct(self):
        Products.objects.create(
            name="Test Product",
            description="description",
            price=10.99,
            image="image.url",
        )

    def test_product_content(self):
        product = Products.objects.get(id=1)
        expected_name = f"{product.name}"
        expected_price = product.price

        self.assertEqual(expected_name, "Test Product")
        self.assertEqual(expected_price, 10.99)
