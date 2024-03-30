import uuid
import datetime

from django.test import TestCase

from products.models import Products


class ProductViewTest(TestCase):
    def setUp(self):
        self.product = Products.objects.create(
            id=uuid.uuid4(),
            name="Test Product",
            description="description",
            price=10.99,
            image="image.url",
            created=datetime.datetime.now(),
        )

    def test_product_content(self):
        product = Products.objects.get(id=self.product.id)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 10.99)
