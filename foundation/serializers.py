from rest_framework import serializers
from .models import Language, Country, Period


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'iso_name', 'iso2', 'iso3', 'native_name', 'alternative_names', 'created_at']


# class CountrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Country
#         fields = ['id', 'iso_name', 'official_state_name', 'iso2', 'iso3', 'native_names', 'alternative_names', 'created_at']
#

class PeriodSerializer(serializers.ModelSerializer):
    countries = serializers.PrimaryKeyRelatedField(many=True, queryset=Country.objects.all())

    class Meta:
        model = Period
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    periods = serializers.PrimaryKeyRelatedField(many=True, queryset=Period.objects.all())

    class Meta:
        model = Country
        fields = '__all__'