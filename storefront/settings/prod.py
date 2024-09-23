from .common import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['amadesa.com', 'www.amadesa.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'amadesa-db',  # Your RDS database name
        'USER': 'postgres',  # Your RDS database user
        'PASSWORD': 'Respublika10!',  # Your RDS database password
        'HOST': 'amadesa-db.cp8a808oguxu.us-east-1.rds.amazonaws.com',  # Your RDS endpoint
        'PORT': '5432',  # PostgreSQL default port
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
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'