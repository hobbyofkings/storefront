# foundation/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LanguageListView, CountryListView, PeriodViewSet

urlpatterns = [
    path('languages/', LanguageListView.as_view(), name='language-list'),
    path('countries/', CountryListView.as_view(), name='country-list'),
]

router = DefaultRouter()
router.register(r'periods', PeriodViewSet)

urlpatterns += [
    path('', include(router.urls)),
]