from rest_framework import serializers
from .models import Language, Country


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'iso_name', 'iso2', 'iso3', 'native_name', 'alternative_names', 'created_at']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'iso_name', 'official_state_name', 'iso2', 'iso3', 'native_names', 'alternative_names', 'created_at']