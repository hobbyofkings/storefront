import json
import datetime
from django.db import transaction, IntegrityError

from .models import (
    Country,
    Entity,
    SovereignStatus,
    HistoricalPeriod,
    Currency,
    AlternativeName, Demonym, CountryLanguage, Language, Continent, EntityClassification)

from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .timeline import prepare_timeline_data




class AlternativeNameInline(admin.TabularInline):
    model = AlternativeName
    extra = 1
    can_delete = True


@admin.register(SovereignStatus)
class SovereignStatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(HistoricalPeriod)
class HistoricalPeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'start_date', 'end_date')
    search_fields = ('name', 'country__name',)
    list_filter = ('country',)

@admin.register(Continent)
class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(EntityClassification)
class EntityClassificationAdmin(admin.ModelAdmin):
    list_display = ('type', 'sovereignty')
    search_fields = ('type', 'sovereignty',)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'entity', 'currency_type', 'start_date', 'end_date')
    search_fields = ('name', 'entity__name', 'currency_type')
    list_filter = ('currency_type', 'entity')

class HistoricalPeriodInline(admin.TabularInline):
    model = HistoricalPeriod
    extra = 1
    can_delete = True

class EntityInline(admin.TabularInline):
    model = Entity
    extra = 1
    can_delete = True

class CurrencyInline(admin.TabularInline):
    model = Currency
    fields = ['name', 'currency_type', 'start_date', 'end_date']
    readonly_fields = ['name', 'currency_type', 'start_date', 'end_date']
    extra = 0

    def get_queryset(self, request):
        # Modify the queryset to fetch currencies related to entities within the country
        country_id = request.resolver_match.kwargs.get('object_id')
        if country_id:
            country = Country.objects.get(pk=country_id)
            return Currency.objects.filter(entity__country=country)
        return Currency.objects.none()



# Inline for managing relationships between countries and languages
class CountryLanguageInline(admin.TabularInline):
    model = CountryLanguage
    extra = 1
    can_delete = True
    readonly_fields = ['get_iso2', 'get_iso3', 'get_native_name']
    max_num = 5  # Limit to 5 inline rows


    # Use select_related to optimize queries for ForeignKey fields
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('language', 'country')
        return queryset


    def get_iso2(self, obj):
        return obj.language.iso2

    get_iso2.short_description = 'ISO2'

    def get_iso3(self, obj):
        return obj.language.iso3

    get_iso3.short_description = 'ISO3'

    def get_native_name(self, obj):
        return obj.language.native_name

    get_native_name.short_description = 'Native Name'



class DemonymInlineForm(forms.ModelForm):
    class Meta:
        model = Demonym
        fields = '__all__'
        widgets = {
            'main_demonym': forms.TextInput(attrs={'size': 30}),
            'alternative_demonyms': forms.Textarea(attrs={'rows': 2, 'cols': 50, 'style': 'resize: vertical;'}),
        }

# Inline for managing relationships between demonyms and countries
class DemonymInline(admin.TabularInline):
    model = Demonym
    form = DemonymInlineForm
    extra = 1
    can_delete = True




# Admin for managing Language with inlines for alternative names and country relationships
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'iso2', 'iso3', 'native_name', 'created_at']
    search_fields = ['name', 'native_name', 'iso2', 'iso3']
    list_filter = ['created_at']
    list_per_page = 25
    inlines = [AlternativeNameInline, CountryLanguageInline]  # Add AlternativeName and CountryLanguage inlines

    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            with transaction.atomic():
                return super().change_view(request, object_id, form_url, extra_context)
        except IntegrityError as e:
            self.message_user(request, f"An error occurred: {e}", level='error')
            return super().changelist_view(request, extra_context=extra_context)


class CountryAdminForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'
        widgets = {
            'native_names': forms.Textarea(attrs={'rows': 2, 'cols': 60, 'style': 'resize: vertical;'}),
            'alternative_names': forms.Textarea(attrs={'rows': 2, 'cols': 60, 'style': 'resize: vertical;'}),
        }

class DemonymAdminForm(forms.ModelForm):
    class Meta:
        model = Demonym
        fields = '__all__'
        widgets = {
            'alternative_demonyms': forms.Textarea(attrs={'rows': 2, 'cols': 60, 'style': 'resize: vertical;'}),
        }


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    form = CountryAdminForm
    list_display = [
        'flag_thumbnail_list',
        'clickable_country_name',
        'iso2',
        'iso3',
        'get_languages',
        'continent',
        'start_date',
        'end_date',
        'created_at'
    ]

    search_fields = ['name', 'iso2', 'iso3']
    list_filter = ['created_at']
    ordering = ['name']
    inlines = [CountryLanguageInline, DemonymInline, HistoricalPeriodInline, EntityInline]  # Removed CurrencyInline

    readonly_fields = ('flag_thumbnail',)
    change_form_template = 'admin/foundation/country/change_form.html'


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related(
            'countrylanguage_set__language',
            'demonyms',
            'historical_periods',
            'entities__currencies',
            'entities__classification'
        )
        return queryset

    def get_languages(self, obj):
        # Use prefetch_related to get all related languages and avoid multiple queries
        return ", ".join([cl.language.name for cl in obj.countrylanguage_set.all()])
    get_languages.short_description = 'Languages'



    def get_demonyms(self, obj):
        return ", ".join([demonym.main_demonym for demonym in obj.demonyms.all()])
    get_demonyms.short_description = 'Demonyms'

    def flag_thumbnail(self, obj):
        # Display a larger version of the flag on the detail page
        if obj.flag:
            return format_html('<img src="{}" width="50" height="auto" />', obj.flag.url)
        return "-"

    flag_thumbnail.short_description = "Flag Thumbnail"

    def flag_thumbnail_list(self, obj):
        # Display a smaller version of the flag in the list view
        if obj.flag:
            return format_html('<img src="{}" width="30" height="auto" />', obj.flag.url)
        return "-"

    flag_thumbnail_list.short_description = "Flag"

    def clickable_country_name(self, obj):
        """ Make the country name a clickable link to edit the country. """
        url = reverse('admin:foundation_country_change', args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.name)
    clickable_country_name.short_description = 'Country Name'

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if not extra_context:
            extra_context = {}

        if object_id:
            country = get_object_or_404(Country, pk=object_id)
            historical_periods = country.historical_periods.all()
            entities = country.entities.all()
            currencies = Currency.objects.filter(entity__in=entities)

            # Prepare timeline data
            timeline_data, categories = prepare_timeline_data(country, historical_periods, entities, currencies)

            extra_context.update({
                'timeline_data': json.dumps(timeline_data),
                'categories': json.dumps(categories),
                'country': country
            })
        else:
            extra_context.update({
                'timeline_data': json.dumps([]),
                'categories': json.dumps([]),
                'country': None
            })

        return super().changeform_view(request, object_id, form_url, extra_context=extra_context)

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'classification', 'start_date', 'end_date')
    search_fields = ('name', 'country__name', 'classification__type')
    list_filter = ('country', 'classification')
    inlines = [CurrencyInline]