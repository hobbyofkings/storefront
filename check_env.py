import os

django_env = os.getenv('DJANGO_ENV', 'not set')
print(f'DJANGO_ENV: {django_env}')