from .common import *

import os
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
import dj_database_url


SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['amadesa-prod-1b5472657019.herokuapp.com']\


DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('CLEARDB_DATABASE_URL')
    )
}

REDIS_URL = os.environ.get('REDIS_URL')

CELERY_BROKER_URL = REDIS_URL
# When using TCP connections
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        'TIMEOUT': 600, # 10 minutes
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
EMAIL_HOST_USER = os.environ['MAILGUN_SMTP_LOGIN']
EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
EMAIL_PORT = os.environ['MAILGUN_SMTP_PORT']