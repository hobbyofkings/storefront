# #!/usr/bin/env python
# """Django's command-line utility for administrative tasks."""
# import os
# import sys
#
#
# def main():
#     """Run administrative tasks."""
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings.prod')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)
#
#
# if __name__ == '__main__':
#     main()

import os
import sys
import dotenv

def main():
    """Run administrative tasks."""
    django_env = os.getenv('DJANGO_ENV', 'development')
    print(f"DJANGO_ENV in manage.py: {django_env}")

    if django_env == 'production':
        dotenv_file = os.path.join(os.path.dirname(__file__), 'storefront', 'settings', '.env')
        print("Loaded production environment in manage.py")
    else:
        dotenv_file = os.path.join(os.path.dirname(__file__), 'storefront', 'settings', '.env.dev')
        print("Loaded development environment in manage.py")

    # Load the appropriate .env file
    dotenv.load_dotenv(dotenv_file)

    # Set the settings module from the loaded environment variables
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'storefront.settings.dev'))

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()