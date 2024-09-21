# its a special file that pytest will look for and execute before running any tests.
import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

# authentification
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate