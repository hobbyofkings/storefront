from rest_framework import generics
from .models import Language, Country
from .serializers import LanguageSerializer, CountrySerializer

class LanguageListView(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class CountryListView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer