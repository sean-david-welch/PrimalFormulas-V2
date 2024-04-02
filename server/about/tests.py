from django.urls import reverse

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
    pass
