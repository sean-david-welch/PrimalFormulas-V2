from django.urls import reverse
from rest_framework import status
from unittest.mock import Mock, patch

from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User

from products.models import Product


class BaseTestMock(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("product-list")
        cls.product_data = {
            "name": "new product",
            "description": "new description",
            "price": 20.99,
            "image": "new_image_placeholder",
        }
        product = Product.objects.create(
            name="Detail Test Product",
            description="Detail Test Description",
            price=59.99,
            image="image_placeholder",
        )
        cls.product_id = product.id
        cls.detail_url = reverse("product-detail", kwargs={"pk": cls.product_id})

    def setUp(self):
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
            "products.views.S3ImageHandler", return_value=mock_s3_handler
        )
        self.patcher.start()
        self.mock_s3_handler = mock_s3_handler

    def create_test_users(self):
        self.superuser = User.objects.create_superuser(
            username="testsuperuser",
            password="testpassword",
            email="testemail@email.com",
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def create_test_products(self):
        Product.objects.bulk_create(
            [
                Product(
                    name="Test Product 1",
                    description="Test Description 1",
                    price=39.99,
                    image="image_placeholder",
                ),
                Product(
                    name="Test Product 2",
                    description="Test Description 2",
                    price=45.99,
                    image="image_placeholder",
                ),
            ]
        )

    def tearDown(self):
        self.patcher.stop()


class ProductListTest(BaseTestMock):
    def test_get_products(self):
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Product.objects.count())

    def test_post_product_with_auth(self):
        self.client.login(username="testsuperuser", password="testpassword")

        response = self.client.post(self.url, data=self.product_data, format="json")

        self.assertPostProductSuccess(response)

    def test_post_product_without_auth(self):
        response = self.client.post(self.url, self.product_data, format="json")

        self.assertPostProductFailure(
            response, expected_status=status.HTTP_401_UNAUTHORIZED
        )

    def assertPostProductSuccess(self, response: Response):
        product_data = response.data.get("product")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("product" in response.data)
        self.assertTrue(self.mock_s3_handler.generate_presigned_url.called)
        self.assertEqual(response.data.get("presigned_url"), "mock_presigned_url")

        self.assertIsNotNone(product_data)
        self.assertIn("image", product_data)
        self.assertEqual(product_data["image"], "mock_image_url")

    def assertPostProductFailure(self, response: Response, expected_status: int):
        self.assertEqual(
            response.status_code,
            expected_status,
            msg=f"Expected status code {expected_status}, got {response.status_code}",
        )


class ProductDetailTest(BaseTestMock):
    def test_get_product_by_id(self):
        response: Response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(str(response.data["id"]), str(self.product_id))

        self.assertEqual(response.data["name"], "Detail Test Product")

    def test_put_product(self):
        self.client.login(username="testsuperuser", password="testpassword")

        response = self.client.put(self.detail_url, self.product_data, format="json")

        self.assertPutProductSuccess(response)

    def test_delete_product(self):
        self.client.login(username="testsuperuser", password="testpassword")

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=self.product_id)

    def assertPutProductSuccess(self, response: Response):
        product_data = response.data.get("product")

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertTrue("product" in response.data)

        self.assertTrue(self.mock_s3_handler.generate_presigned_url.called)
        self.assertEqual(response.data.get("presigned_url"), "mock_presigned_url")

        self.assertIsNotNone(product_data)
        self.assertIn("image", product_data)
        self.assertEqual(product_data["image"], "mock_image_url")
