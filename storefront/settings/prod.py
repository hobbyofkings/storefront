from .common import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = ['amadesa.com', 'www.amadesa.com']

DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE', default='django.db.backends.postgresql'),
        'NAME': env('DATABASE_NAME', default='amadesa-db'),
        'USER': env('DATABASE_USER', default='postgres'),
        'PASSWORD': env('DATABASE_PASSWORD', default='Respublika10!'),
        'HOST': env('DATABASE_HOST', default='amadesa-db.cp8a808oguxu.us-east-1.rds.amazonaws.com'),
        'PORT': env('DATABASE_PORT', default='5432'),
    }
}

# Comment out Redis settings for now
# REDIS_URL = os.environ.get('REDIS_URL')
# CELERY_BROKER_URL = REDIS_URL

# Comment out the cache settings if you are not using Redis for now
# CACHES = {
#    "default": {
#        "BACKEND": "django_redis.cache.RedisCache",
#        "LOCATION": REDIS_URL,
#        "TIMEOUT": 600,  # 10 minutes
#        "OPTIONS": {
#            "CLIENT_CLASS": "django_redis.client.DefaultClient",
#        }
#    }
# }

# Static and media files on S3 (if using)
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'