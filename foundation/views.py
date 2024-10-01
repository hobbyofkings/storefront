# foundation/views.py
from rest_framework import generics, viewsets
from .models import Language, Country, Period
from .serializers import LanguageSerializer, CountrySerializer, PeriodSerializer

class LanguageListView(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class CountryListView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class PeriodViewSet(viewsets.ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer