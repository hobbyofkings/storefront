# foundation/views.py
from rest_framework import generics, viewsets
from .models import Language, Country
from .serializers import LanguageSerializer, CountrySerializer

class LanguageListView(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class CountryListView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer





from django.shortcuts import render, get_object_or_404
from .models import Country, Entity, HistoricalPeriod
def country_detail(request, pk):
    # Fetch the country using the primary key (pk)
    country = get_object_or_404(Country, pk=pk)

    # Fetch entities related to the country
    entities = Entity.objects.filter(
        parent_entity__countries__country=country
    ).select_related(
        'parent_entity', 'sovereign_status', 'entity_type'
    ).prefetch_related(
        'historical_periods'
    ).distinct()

    # Initialize an empty list to hold the processed data
    timeline_data = []

    # Loop through each entity associated with the country
    for entity in entities:
        # Fetch historical periods associated with the entity
        periods = entity.historical_periods.all()

        # Create a dictionary with the necessary information
        data_point = {
            'entity_name': entity.name,
            'start_date': entity.start_date,
            'end_date': entity.end_date,
            'historical_periods': [p.name for p in periods],
        }

        # Add the dictionary to the timeline_data list
        timeline_data.append(data_point)

    # Prepare the context to pass to the template
    context = {
        'country': country,
        'timeline_data': timeline_data,
    }

    # Render the template with the context data
    return render(request, 'country_detail.html', context)






