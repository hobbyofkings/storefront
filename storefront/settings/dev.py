from .common import *  # Import all shared settings from common.py

# Override specific settings for development here
DEBUG = True
ROOT_URLCONF = 'storefront.urls'
CELERY_BROKER_URL = 'redis://localhost:6379/1'  # or your chosen broker
# When using TCP connections
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        'TIMEOUT': 600,  # 10 minutes
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525


print(f"Database Name: {DATABASES['default']['NAME']}")
print(f"Database User: {DATABASES['default']['USER']}")
print(f"Database Host: {DATABASES['default']['HOST']}")