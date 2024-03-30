import os

from typing import Tuple
from boto3 import client


def generate_presigned_url(folder: str, image: str) -> Tuple[str, str]:
    bucket_name = "primalformulas.ie"
    cloudfront_name = "www.primalformulas.ie"

    image_key = f"images/{folder}/{image}"
    image_url = f"https://{cloudfront_name}/{image_key}"

    s3_client = client(
        service_name="s3",
        region_name="eu-west-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        presigned_url = s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": bucket_name, "Key": image_key},
            ExpiresIn=300,
        )
    except Exception as error:
        raise Exception(f"Error generating presigned URL: {error}") from error

    return image_url, presigned_url
