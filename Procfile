web: gunicorn storefront.wsgi --log-file -
release: python manage.py migrate
worker: celery -A storefront worker -l info