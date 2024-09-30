from django.urls import path
from .views import LanguageListView, CountryListView

urlpatterns = [
    path('languages/', LanguageListView.as_view(), name='language-list'),
    path('countries/', CountryListView.as_view(), name='country-list'),

]