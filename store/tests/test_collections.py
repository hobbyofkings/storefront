
from rest_framework import status
import pytest
from django.contrib.auth.models import User
from store.models import Collection, Product
from model_bakery import baker

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)

    return do_create_collection



@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        response = create_collection({'title': 'a'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, create_collection, authenticate):
        authenticate()
        response = create_collection({'title': 'a'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, api_client, create_collection, authenticate):

        authenticate(is_staff=True)
        response = create_collection({'title': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None


    def test_if_data_is_valid_returns_201(self, api_client, create_collection,authenticate):

        authenticate(is_staff=True)
        response = api_client.post('/store/collections/', {'title': 'a'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0



@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exist_returns_200(self, api_client):
        collection = baker.make(Collection)
        response = api_client.get(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0
        }

    def test_if_collection_does_not_exist_returns_404(self, api_client):
        response = api_client.get('/store/collections/1/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_collection_has_products_returns_200(self, api_client):
        collection = baker.make(Collection)
        baker.make(Product, collection=collection, _quantity=2)
        response = api_client.get(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['products_count'] == 2


