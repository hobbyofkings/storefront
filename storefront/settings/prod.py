from django.core.exceptions import ImproperlyConfigured

from .common import *

import os
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['amadesa-prod.herokuapp.com']

DATABASE_URL = os.environ.get('DATABASE_URL')

# Explicit database engine specification along with database URL
if DATABASE_URL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',  # Explicitly specify PostgreSQL engine
            **dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True),
        }
    }
else:
    raise ImproperlyConfigured("DATABASE_URL environment variable not set.")

# Redis settings
REDIS_URL = os.environ.get('REDIS_URL')

CELERY_BROKER_URL = REDIS_URL

# Cache settings
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        'TIMEOUT': 600,  # 10 minutes
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Email settings using Mailgun
EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
EMAIL_HOST_USER = os.environ['MAILGUN_SMTP_LOGIN']
EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
EMAIL_PORT = os.environ['MAILGUN_SMTP_PORT']