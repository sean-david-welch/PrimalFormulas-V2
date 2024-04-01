from unittest.mock import Mock, patch
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User

from products.models import Product


class ProductListTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("products-list")
        cls.product_data = {
            "name": "new product",
            "description": "new description",
            "price": 20.99,
            "image": "image_placeholder",
        }

    def setUp(self) -> None:
        self.client = APIClient()

        self.mock_s3_handler_setup()
        self.create_test_users()
        self.create_test_products()

    def mock_s3_handler_setup(self):
        mock_s3_handler = Mock(
            generate_presigned_url=Mock(
                return_value=("mock_image_url", "mock_presigned_url")
            )
        )
        self.patcher = patch(
            "primalformulas.images.S3ImageHandler", return_value=mock_s3_handler
        )
        self.patcher.start()
        self.mock_s3_handler = mock_s3_handler

    def create_test_users(self):
        self.superuser = User.objects.create_superuser(
            username="testsuperuser", password="testpassword"
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def create_test_products(self):
        Product.objects.bulk_create(
            [
                Product(
                    name="Test Product 1", description="Test Description 1", price=39.99
                ),
                Product(
                    name="Test Product 2", description="Test Description 2", price=45.99
                ),
            ]
        )

    def tearDown(self) -> None:
        self.patcher.stop()

    def test_get_products(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Product.objects.count())

    def test_post_product_with_auth(self) -> None:
        self.client.login(username="testsuperuser", password="testpassword")

        response: Response = self.client.post(
            self.url, data=self.product_data, format="json"
        )

        self.assertPostProductSuccess(response)

    def assertPostProductSuccess(self, response: Response) -> None:
        product_data = response.data.get("product")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("product" in response.data)
        self.assertTrue(self.mock_s3_handler.generate_presigned_url.called)
        self.assertEqual(response.data.get("presigned_url"), "mock_presigned_url")

        self.assertIsNotNone(product_data)
        self.assertIn("image", product_data)
        self.assertEqual(product_data["image"], "mock_image_url")

    def test_post_product_without_auth(self):
        url = reverse("product-list")
        data = {
            "name": "Unauthorized Product",
            "description": "Should not be created",
            "price": 400,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
