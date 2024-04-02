from unittest.mock import Mock, patch
from django.contrib.auth.models import User


class TestUtilityMixin:
    def mock_s3_handler_setup(self, app_name: str) -> None:
        mock_s3_handler = Mock(
            generate_presigned_url=Mock(
                return_value=("mock_image_url", "mock_presigned_url")
            )
        )
        patch_path = f"{app_name}.views.S3ImageHandler"

        self.patcher = patch(patch_path, return_value=mock_s3_handler)
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

    def tearDown(self):
        self.patcher.stop()
