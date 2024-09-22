from .common import *
import os
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['amadesa-prod.herokuapp.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'Amadesa'),  # The name of your database on RDS
        'USER': os.getenv('DB_USER', 'postgres'),  # The username for your RDS instance
        'PASSWORD': os.getenv('DB_PASSWORD', ''),  # The password for your RDS instance
        'HOST': os.getenv('DB_HOST', 'amadesa-db.cp8a808oguxu.us-east-1.rds.amazonaws.com'),  # Your RDS endpoint
        'PORT': os.getenv('DB_PORT', '5432'),  # Default PostgreSQL port
    }
}

# Redis settings
REDIS_URL = os.environ.get('REDIS_URL')
CELERY_BROKER_URL = REDIS_URL

# Cache settings
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": 600,  # 10 minutes
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# # Email settings using Mailgun
# EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
# EMAIL_HOST_USER = os.environ['MAILGUN_SMTP_LOGIN']
# EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
# EMAIL_PORT = os.environ['MAILGUN_SMTP_PORT']