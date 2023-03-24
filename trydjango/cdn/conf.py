import os

AWS_ACCESS_KEY_ID=os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME=os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_LOCATION = "staticfiles"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_S3_ENDPOINT_URL = "https://django-delights.ams3.digitaloceanspaces.com"

AWS_DEFAULT_ACL = 'public-read'

AWS_S3_SIGNATURE_VERSION = 's3v4'

DEFAULT_FILE_STORAGE = "trydjango.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "trydjango.cdn.backends.StaticRootS3Boto3Storage"

STATIC_ROOT = 'staticfiles/'
MEDIA_ROOT = 'mediafiles'
STATIC_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, STATIC_ROOT)
MEDIA_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, MEDIA_ROOT)
