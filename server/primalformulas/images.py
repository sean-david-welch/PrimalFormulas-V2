import boto3

from django.conf import settings
from urllib.parse import urlparse
from botocore.exceptions import ClientError


class S3ImageHandler:
    def __init__(self, region_name="eu-west-1") -> None:
        self.bucket_name = "primalformulas.ie"
        self.s3_client = boto3.client(
            service_name="s3",
            region_name=region_name,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def generate_presigned_url(self, folder: str, image: str) -> tuple:
        cloudfront_name = "www.primalformulas.ie"

        image_key = f"images/{folder}/{image}"
        image_url = f"https://{cloudfront_name}/{image_key}"

        try:
            presigned_url = self.s3_client.generate_presigned_url(
                "put_object",
                Params={"Bucket": self.bucket_name, "Key": image_key},
                ExpiresIn=300,
            )
        except Exception as error:
            raise Exception(f"Error generating presigned URL: {error}") from error

        return image_url, presigned_url

    def delete_image_from_s3(self, image_url: str) -> bool:
        try:
            parsed_url = urlparse(image_url)
            image_key = parsed_url.path.lstrip("/")
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=image_key)
        except ClientError as error:
            print(f"Error deleting object from S3: {error}")
            return False

        return True
