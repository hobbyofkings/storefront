from .common import *
import os
from pathlib import Path




# Override DEBUG setting
DEBUG = get_env_variable('DEBUG') == 'False'



# print("DJANGO_SECRET_KEY in common.py:", SECRET_KEY)
# print(f"common.py DEBUG: {DEBUG}")


ALLOWED_HOSTS = ['amadesa.com', 'www.amadesa.com', '67.202.22.239', '127.0.0.1', 'localhost', '*']
CSRF_TRUSTED_ORIGINS = ['https://amadesa.com', 'https://www.amadesa.com']
ROOT_URLCONF = 'storefront.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable('DATABASE_NAME'),
        'USER': get_env_variable('DATABASE_USER'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
        'HOST': get_env_variable('DATABASE_HOST'),
        'PORT': get_env_variable('DATABASE_PORT'),
    }
}


AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'amadesa'


STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        'OPTIONS': {
            'access_key': get_env_variable('AWS_ACCESS_KEY_ID'),
            'secret_key': get_env_variable('AWS_SECRET_ACCESS_KEY'),
            'bucket_name': AWS_STORAGE_BUCKET_NAME,
        },
    },
    'staticfiles': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
    },
}


# Media files on S3
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Static files stored locally
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# If you want to store media files locally instead of S3, use these settings:
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Set up the log directory


LOG_DIR = os.getenv('LOG_DIR', default=os.path.join(BASE_DIR, 'logs'))
log_path = Path(LOG_DIR)

# Create the log directory if it does not exist
if not log_path.exists():
    try:
        log_path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(f"Permission denied when creating log directory: {LOG_DIR}")

# LOGGING configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} ({levelname}) - {name} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': str(log_path / 'error.log'),  # Use the Path object for cleaner path handling
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
    },
}





# LOG_DIR = os.getenv('LOG_DIR', default=BASE_DIR / 'logs')
#
# # Create the log directory if it does not exist
# Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
#
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'WARNING',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(LOG_DIR, 'error.log'),
#         },
#     },
#     'root': {
#         'handlers': ['file'],
#         'level': 'WARNING',
#     },
#     'django': {
#         'handlers': ['file'],
#         'level': 'WARNING',
#         'propagate': False,
#     },
# }