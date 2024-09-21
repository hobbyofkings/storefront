release: python manage.py migrate
web: waitress-serve --port=$PORT storefront.wsgi:application
worker: celery -A storefront worker -l info