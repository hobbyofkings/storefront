from .common import *
import os
from pathlib import Path




# Override DEBUG setting
DEBUG = get_env_variable('DEBUG') == 'False'



# print("DJANGO_SECRET_KEY in common.py:", SECRET_KEY)
# print(f"common.py DEBUG: {DEBUG}")


ALLOWED_HOSTS = ['amadesa.com', 'www.amadesa.com', '67.202.22.239', '127.0.0.1', 'localhost', '*']
CSRF_TRUSTED_ORIGINS = ['https://amadesa.com', 'https://www.amadesa.com']


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








# Store static files locally
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Store media files locally
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

