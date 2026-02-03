from datetime import datetime

import boto3

from app.core.config import settings


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.minio_endpoint,
        aws_access_key_id=settings.minio_root_user,
        aws_secret_access_key=settings.minio_root_password,
        region_name=settings.minio_region,
    )


def ensure_bucket() -> None:
    client = get_s3_client()
    buckets = [bucket["Name"] for bucket in client.list_buckets().get("Buckets", [])]
    if settings.minio_bucket not in buckets:
        client.create_bucket(Bucket=settings.minio_bucket)


def upload_bytes(content: bytes, filename: str, content_type: str) -> str:
    ensure_bucket()
    key = f"{datetime.utcnow().isoformat()}-{filename}"
    client = get_s3_client()
    client.put_object(Bucket=settings.minio_bucket, Key=key, Body=content, ContentType=content_type)
    return f"{settings.minio_endpoint}/{settings.minio_bucket}/{key}"
