from django.urls import reverse
from django.utils.text import slugify

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase
from primalformulas.mixins import TestUtilityMixin
from assets.models import Asset


class BaseTestMock(APITestCase, TestUtilityMixin):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        cls.url = reverse("asset-list")
        cls.asset_data = {"name": "name", "content": "newcontent"}

        asset = Asset.objects.create(name="assetdetail", content="DetailContent")
        cls.asset_name = asset.name
        cls.detail_url = reverse(
            "asset-detail", kwargs={"name": slugify(cls.asset_name)}
        )

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()

        self.mock_s3_handler_setup("assets")
        self.create_test_users()
        self.create_test_assets()

    def tearDown(self) -> None:
        super().tearDown()

    def create_test_assets(self):
        Asset.objects.bulk_create(
            [
                Asset(name="asset1", content="Test_Content_1"),
                Asset(name="asset2", content="Test_Content_2"),
            ]
        )


class AssetListTest(BaseTestMock):
    def test_get_assets(self):
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Asset.objects.count())

    def test_post_asset_with_auth(self):
        self.client.login(username="testsuperuser", password="testpassword")

        response: Response = self.client.post(
            self.url, data=self.asset_data, format="json"
        )

        self.assertPostAssetSuccess(response)

    def test_post_asset_without_auth(self):
        response: Response = self.client.post(self.url, self.asset_data, format="json")

        self.assertPostAssetFailure(
            response, expected_status=status.HTTP_401_UNAUTHORIZED
        )

    def assertPostAssetSuccess(self, response: Response):
        asset_data = response.data.get("asset")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("asset" in response.data)

        self.assertTrue(self.mock_s3_handler.generate_presigned_url.called)
        self.assertEqual(response.data.get("presigned_url"), "mock_presigned_url")

        self.assertIsNotNone(asset_data)
        self.assertIn("content", asset_data)
        self.assertEqual(asset_data["content"], "mock_image_url")

    def assertPostAssetFailure(self, response: Response, expected_status: int):
        self.assertEqual(
            response.status_code,
            expected_status,
            msg=f"expected_status: {expected_status}, got: {response.status_code}",
        )


class AssetDetailTest(BaseTestMock):
    def test_get_asset_by_name(self):
        response: Response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data["name"]), str(self.asset_name))

        self.assertEqual(response.data["name"], "assetdetail")

    def test_put_asset(self):
        self.client.login(username="testsuperuser", password="testpassword")

        response: Response = self.client.put(
            self.detail_url, self.asset_data, format="json"
        )

        self.assertPutAssetSuccess(response)

    def test_delete_asset(self):
        self.client.login(username="testsuperuser", password="testpassword")

        response: Response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Asset.DoesNotExist):
            Asset.objects.get(name=self.asset_name)

    def assertPutAssetSuccess(self, response: Response):
        asset_data = response.data.get("asset")

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertTrue("asset" in response.data)

        self.assertTrue(self.mock_s3_handler.generate_presigned_url.called)
        self.assertEqual(response.data.get("presigned_url"), "mock_presigned_url")

        self.assertIsNotNone(asset_data)
        self.assertIn("content", asset_data)
        self.assertEqual(asset_data["content"], "mock_image_url")
