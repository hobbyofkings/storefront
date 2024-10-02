from datetime import timedelta
from pathlib import Path
import os
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseForbidden
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent  # Points to storefront3/storefront/

# Load the .env file
load_dotenv(os.path.join(BASE_DIR, 'settings', '.env'))
ALLOWED_ADMIN_IPS = os.getenv('ALLOWED_ADMIN_IPS', '').split(',')

class AdminIPRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        print(f"Request IP: {ip}")  # Debug print to see the IP address
        if request.path.startswith('/admin/'):
            if ip not in ALLOWED_ADMIN_IPS:
                return HttpResponseForbidden("You are not allowed to access this page.")
        return self.get_response(request)





def get_env_variable(var_name):
    value = os.getenv(var_name)
    if not value:
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)
    return value


SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')
# print("DJANGO_SECRET_KEY in common.py:", os.getenv('DJANGO_SECRET_KEY'))


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

DEBUG = get_env_variable('DEBUG') == 'True'
print(f"common.py DEBUG: {DEBUG}")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'corsheaders',
    'rest_framework',
    'djoser',
    'silk',
    'storages',
    'playground',
    # 'debug_toolbar',
    'store',
    'tags',
    'likes',
    'core',
    'foundation'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'silk.middleware.SilkyMiddleware',
    'storefront.settings.common.AdminIPRestrictionMiddleware',

]




# if DEBUG:
#     INSTALLED_APPS += ['silk']
#     MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

INTERNAL_IPS = [
    '127.0.0.1',

]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8001",
]

DEFAULT_FROM_EMAIL = 'listingas@gmail.com'
ADMINS = [
    ('Admin', 'listingas@gmail.com'),
]

ROOT_URLCONF = 'storefront.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'storefront.wsgi.application'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Remove the brackets

MEDIA_URL = '/media/' #my own server (pc, with x 6 HDD 20 TB, NAS)
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

AUTH_USER_MODEL = 'core.User'

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'core.serializers.UserCreateSerializer',
        'current_user': 'core.serializers.UserSerializer',
    }
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1)
}

CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_BEAT_SCHEDULE = {
    'notify_customers': {
        'task': 'playground.tasks.notify_customers',
        'schedule': timedelta(seconds=1),
        'args': ('Hello there, im beat worker, scheduler!',)

    }
}


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




AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'amadesa'
# if DEBUG:
#     print("DJANGO_SECRET_KEY in common.py:", SECRET_KEY)
#     print(f"common.py DEBUG: {DEBUG}")

# Static and media files on S3
STORAGES = {'staticfiles': {'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage'}}


AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

ADDMIN_MEDIA_PREFIX = '/static/admin/'

