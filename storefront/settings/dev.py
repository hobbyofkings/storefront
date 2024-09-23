from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SECRET_KEY = 'qkykzo'
# (venv) ubuntu@ip-172-31-39-33:~/storefront$ python -c 'import secrets; print(secrets.token_urlsafe())'
# pNsEJHemPEb70E3sEw9prAclVDcw5NhK6470XJxazL0


CELERY_BROKER_URL = 'redis://localhost:6379/1'  # or your chosen broker
# When using TCP connections
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        'TIMEOUT': 600, # 10 minutes
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525