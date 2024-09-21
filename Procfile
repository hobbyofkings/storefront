release: python manage.py migrate
web: waitress-serve --port=$PORT storefront3.wsgi:application
worker: celery -A storefront worker -l info