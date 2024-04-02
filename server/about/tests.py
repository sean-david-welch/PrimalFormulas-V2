from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

from about.models import About
from primalformulas.mixins import TestUtilityMixin


class BaseTestMock(APITestCase, TestUtilityMixin):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("about-list")
        cls.about_data = {
            "title": "new about",
            "description": "new about description",
            "image": "new_image_placeholder",
        }

        about: About = About.objects.create(
            title="Detail about", description="Detail description", image="Detail image"
        )
        cls.about_id = (about.id,)
        cls.detail_url = reverse("about-detail", kwargs={"pk": cls.about_id})

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()

        self.mock_s3_handler_setup("about")
        self.create_test_users()
        self.create_test_about()

    def tearDown(self):
        super().tearDown()

    def create_test_about(self):
        About.objects.bulk_create(
            [
                About(
                    title="Test About 1",
                    description="Test description 1",
                    image="image_placeholder",
                ),
                About(
                    title="Test About 2",
                    description="Test description 2",
                    image="image_placeholder",
                ),
            ]
        )


class AboutListTest(BaseTestMock):
    def test_get_about(self):
        response: Response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), About.objects.count())

    def test_post_about_with_auth(self):
        self.client.login(username="testsuperuser", password="testpassword")

        response = self.client.post(self.url, data=self.about_data, format="json")

        self.assertPostAboutSuccess(response)

    def test_post_about_without_auth(self):
        response = self.client.post(self.url, self.about_data, format="json")

        self.assertPostAboutFailure(
            response, expected_status=status.HTTP_401_UNAUTHORIZED
        )

    def assertPostAboutSuccess(self, response: Response):
        about_data = response.data.get("about")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("about" in about_data)

        self.assertTrue(self.mock_s3_handler.generate_presigned_url.called)
        self.assertEqual(response.data.get("presigned_url"), "mock_presigned_url")

        self.assertIsNotNone(about_data)
        self.assertIn("image", about_data)
        self.assertEqual(about_data["image"], "mock_image_url")

    def assertPostAboutFailure(self, response: Response, expected_status: int):
        self.assertEqual(
            response.status_code,
            expected_status,
            msg=f"Excpected status code {expected_status}, got {response.status_code}",
        )


class AboutDetailTest(BaseTestMock):
    def test_get_about_by_id(self):
        response: Response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data["id"]), str(self.about_id))
        self.assertEqual(response.data["title"], "Detail About")

    def test_put_about(self):
        self.client.login(username="testsuperuser", password="testpassword")

        response: Response = self.client.put(
            self.detail_url, self.about_data, format="json"
        )

        self.assertPutAboutSuccess(response)

    def test_delete_about(self):
        self.client.login(username="testsuperuser", password="testpassword")

        response: Response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(About.DoesNotExist):
            About.objects.get(id=self.about_id)

    def assertPutAboutSuccess(self, response: Response):
        about_data = response.data.get("about")

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertTrue("about" in response.data)

        self.assertTrue(self.mock_s3_handler.generate_presigned_url.called)
        self.assertEqual(response.data.get("presigned_url"), "mock_presigned_url")

        self.assertIsNotNone(about_data)
        self.assertIn("image", about_data)
        self.assertEqual(about_data["image"], "mock_image_url")
