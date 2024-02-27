from boto3 import client
from utils.config import settings


def generate_presigned_url(folder: str, image: str) -> str:
    bucket_name = "primalformulas.ie"
    cloudfront_name = "primalformulas.ie"

    image_key = f"{folder}/{image}"
    image_url = f"{cloudfront_name}/{image_key}"

    s3_client = client(
        "s3",
        region_name="eu-west-1",
        aws_access_key_id=settings["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=settings["AWS_SECRET_ACCESS_KEY"],
    )

    try:
        response = s3_client.generate_presigned_post(
            Bucket=bucket_name, Key=image_key, ExpiresIn=300
        )

        return {"image_url": image_url, "presinged_url": response.get("url")}
    except Exception as error:
        raise Exception(f"Error generating presigned URL: {error}") from error
