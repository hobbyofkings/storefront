release: python manage.py migrate
web: gunicorn storefront.wsgi:application --log-file -
worker: celery -A storefront worker -l info