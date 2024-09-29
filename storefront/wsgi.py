# """
# WSGI config for storefront project.
#
# It exposes the WSGI callable as a module-level variable named ``application``.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
# """
#
# import os
#
# from django.core.wsgi import get_wsgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings.prod')
#
# application = get_wsgi_application()
#
# print('WSGI loaded. name of the settings module:', os.environ.get('DJANGO_SETTINGS_MODULE'))

import os
import dotenv
from django.core.wsgi import get_wsgi_application

# Determine which environment to load
django_env = os.getenv('DJANGO_ENV', 'development')
print(f"DJANGO_ENV in wsgi: {django_env}")

if django_env == 'production':
    dotenv_file = os.path.join(os.path.dirname(__file__), 'storefront', 'settings', '.env')
    print("Loaded production environment in wsgi")
else:
    dotenv_file = os.path.join(os.path.dirname(__file__), 'storefront', 'settings', '.env.dev')
    print("Loaded development environment in wsgi")

# Load the appropriate .env file
dotenv.load_dotenv(dotenv_file)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'storefront.settings.prod'))

application = get_wsgi_application()

print('WSGI loaded. name of the settings module:', os.environ.get('DJANGO_SETTINGS_MODULE'))