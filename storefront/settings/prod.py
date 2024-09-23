from .common import *
import os

# SECURITY WARNING: don't run with debug turned on in production!

import environ
env = environ.Env(
    DEBUG=(bool, False)
)

# Reading the .env file
environ.Env.read_env()

# Load the SECRET_KEY from .env
SECRET_KEY = env('SECRET_KEY')


ALLOWED_HOSTS = ['amadesa.com', 'www.amadesa.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Make sure this line is correct
        'NAME': env('DATABASE_NAME', default='amadesa'),
        'USER': env('DATABASE_USER', default='postgres'),
        'PASSWORD': env('DATABASE_PASSWORD', default='Respublika10!'),
        'HOST': env('DATABASE_HOST', default='amadesa-db.cp8a808oguxu.us-east-1.rds.amazonaws.com'),
        'PORT': env('DATABASE_PORT', default='5432'),
        'OPTIONS': {
    'sslmode': 'require',  # Enable SSL
    'sslrootcert': os.path.join(BASE_DIR, 'rds-ca-bundle.pem'),  # Path to the certificate
        }
    }
}


print(f"SECRET_KEY: {env('SECRET_KEY')}")
print(f"DATABASE_NAME: {env('DATABASE_NAME')}")
print(f"DATABASE_USER: {env('DATABASE_USER')}")
print(f"DATABASE_HOST: {env('DATABASE_HOST')}")

# Store static files locally
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Store media files locally
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



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
# AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = 'us-east-1'
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
#
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'