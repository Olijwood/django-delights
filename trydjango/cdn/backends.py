from storages.backends.s3boto3 import S3Boto3Storage
from trydjango.cdn.conf import AWS_STORAGE_BUCKET_NAME

class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = 'staticfiles'
    bucket_name = AWS_STORAGE_BUCKET_NAME

class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = 'mediafiles'
    bucket_name = AWS_STORAGE_BUCKET_NAME