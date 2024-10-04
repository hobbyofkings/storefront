import json
import datetime
from django.utils import timezone
from django.db import transaction, IntegrityError
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Country,
    Entity,
    SovereignStatus,
    HistoricalPeriod,
    Currency,
    AlternativeName, Demonym, CountryLanguage, Language, Continent, EntityClassification)

from django.core.cache import cache
from django import forms
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Currency
from django.contrib import admin
from django.urls import path
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils import timezone





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

    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     if not extra_context:
    #         extra_context = {}
    #
    #     if object_id:
    #         # Existing object (Change view)
    #         country = get_object_or_404(Country, pk=object_id)
    #
    #         # Fetch related historical periods
    #         historical_periods = country.historical_periods.all()
    #
    #         # Fetch related entities
    #         entities = country.entities.all()
    #
    #         # Fetch related currencies
    #         currencies = Currency.objects.filter(entity__in=entities)
    #
    #         # Prepare timeline data
    #         timeline_data, categories = self.prepare_timeline_data(country, historical_periods, entities, currencies)
    #
    #         # Add timeline data and categories to context as JSON
    #         extra_context['timeline_data'] = json.dumps(timeline_data)
    #         extra_context['categories'] = json.dumps(categories)
    #         extra_context['country'] = country
    #     else:
    #         # Add view
    #         extra_context['timeline_data'] = json.dumps([])
    #         extra_context['categories'] = json.dumps([])
    #         extra_context['country'] = None
    #
    #     return super().changeform_view(
    #         request, object_id, form_url, extra_context=extra_context
    #     )
    #
    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     if not extra_context:
    #         extra_context = {}
    #
    #     if object_id:
    #         # Existing object (Change view)
    #         country = get_object_or_404(Country, pk=object_id)
    #
    #         # Fetch related historical periods
    #         historical_periods = country.historical_periods.all()
    #
    #         # Fetch related entities
    #         entities = country.entities.all()
    #
    #         # Fetch related currencies via entities
    #         currencies = Currency.objects.filter(entity__in=entities)
    #
    #         # Prepare timeline data
    #         timeline_data, categories = self.prepare_timeline_data(country, historical_periods, entities, currencies)
    #
    #         # Add timeline data and categories to context as JSON
    #         extra_context['timeline_data'] = json.dumps(timeline_data)
    #         extra_context['categories'] = json.dumps(categories)
    #         extra_context['country'] = country
    #     else:
    #         # Add view
    #         extra_context['timeline_data'] = json.dumps([])
    #         extra_context['categories'] = json.dumps([])
    #         extra_context['country'] = None
    #
    #     return super().changeform_view(
    #         request, object_id, form_url, extra_context=extra_context
    #     )
    #
    # def prepare_timeline_data(self, country, historical_periods, entities, currencies):
    #     timeline_data = []
    #     categories = []
    #     current_timestamp = int(timezone.now().timestamp()) * 1000  # Current timestamp in milliseconds
    #
    #     # Determine the timeline's end date
    #     timeline_end_date = country.end_date if country.end_date else timezone.now().date()
    #
    #     # Helper function to convert date to UTC timestamp in milliseconds
    #     def date_to_utc(date_obj):
    #         if date_obj:
    #             # Combine the date with midnight time to create a datetime object
    #             dt = datetime.datetime.combine(date_obj, datetime.time.min)
    #             # Make the datetime object timezone-aware in UTC
    #             dt = timezone.make_aware(dt, datetime.timezone.utc)
    #             # Return timestamp in milliseconds
    #             return int(dt.timestamp()) * 1000
    #         return None
    #
    #     # Collect all events with their start_date and end_date
    #     events = []
    #
    #     # Add Country event if it has both start and end dates
    #     if country.start_date and country.end_date:
    #         events.append({
    #             'name': f"Country: {country.name}",
    #             'unique_name': f"Country: {country.name} ({country.id})",  # Ensure uniqueness
    #             'start': date_to_utc(country.start_date),
    #             'end': date_to_utc(country.end_date),
    #             'level': 0,
    #             'color': '#4CAF50'  # Updated color for Country
    #         })
    #     elif country.start_date:
    #         events.append({
    #             'name': f"Country: {country.name}",
    #             'unique_name': f"Country: {country.name} ({country.id})",
    #             'start': date_to_utc(country.start_date),
    #             'end': current_timestamp,  # Set to current date if no end_date
    #             'level': 0,
    #             'color': '#4CAF50'
    #         })
    #
    #     # Add Historical Periods if they have both start and end dates
    #     for period in historical_periods:
    #         if period.start_date and period.end_date:
    #             events.append({
    #                 'name': f"Historical Period: {period.name}",
    #                 'unique_name': f"Historical Period: {period.name} ({period.id})",
    #                 'start': date_to_utc(period.start_date),
    #                 'end': date_to_utc(period.end_date),
    #                 'level': 1,
    #                 'color': '#2196F3'  # Updated color for Historical Period
    #             })
    #
    #     # Add Entities and their Currencies if they have both start and end dates
    #     for entity in entities:
    #         if entity.start_date and entity.end_date:
    #             events.append({
    #                 'name': f"Entity: {entity.name}",
    #                 'unique_name': f"Entity: {entity.name} ({entity.id})",
    #                 'start': date_to_utc(entity.start_date),
    #                 'end': date_to_utc(entity.end_date),
    #                 'level': 2,
    #                 'color': '#FFC107'  # Updated color for Entity
    #             })
    #
    #             # Fetch currencies related to the entity that have both start and end dates
    #             entity_currencies = entity.currencies.filter(start_date__isnull=False, end_date__isnull=False)
    #             for currency in entity_currencies:
    #                 events.append({
    #                     'name': f"Currency: {currency.name}",
    #                     'unique_name': f"Currency: {currency.name} ({currency.id})",
    #                     'start': date_to_utc(currency.start_date),
    #                     'end': date_to_utc(currency.end_date),
    #                     'level': 3,
    #                     'color': '#E91E63'  # Updated color for Currency
    #                 })
    #
    #     if not events:
    #         # No valid events to display
    #         return timeline_data, categories
    #
    #     # Sort events by start_date
    #     events.sort(key=lambda x: x['start'] if x['start'] else 0)
    #
    #     # Assign categories and y index
    #     for event in events:
    #         categories.append(event['unique_name'])  # Use unique_name to ensure uniqueness
    #         timeline_data.append(event)
    #
    #     # Remove duplicates in categories while preserving order
    #     seen = set()
    #     categories = [x for x in categories if not (x in seen or seen.add(x))]
    #
    #     # Assign y index to each category
    #     category_indices = {category: index for index, category in enumerate(categories)}
    #
    #     # Now, update timeline_data with 'y' index
    #     for event in timeline_data:
    #         event['y'] = category_indices[event['unique_name']]
    #
    #     return timeline_data, categories


    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if not extra_context:
            extra_context = {}

        if object_id:
            country = get_object_or_404(Country, pk=object_id)

            # Fetch related data in one go to reduce repeated queries
            historical_periods = country.historical_periods.all()
            entities = country.entities.all()
            currencies = Currency.objects.filter(entity__in=entities)

            # Prepare timeline data
            timeline_data, categories = self.prepare_timeline_data(country, historical_periods, entities, currencies)

            # Add prepared data to the context
            extra_context.update({
                'timeline_data': json.dumps(timeline_data),
                'categories': json.dumps(categories),
                'country': country
            })
        else:
            # For add view
            extra_context.update({
                'timeline_data': json.dumps([]),
                'categories': json.dumps([]),
                'country': None
            })

        return super().changeform_view(request, object_id, form_url, extra_context=extra_context)

    def prepare_timeline_data(self, country, historical_periods, entities, currencies):
        import logging
        logger = logging.getLogger(__name__)

        timeline_data = []
        categories = []
        current_timestamp = int(timezone.now().timestamp()) * 1000  # Current timestamp in milliseconds

        # Helper function to convert date to UTC timestamp in milliseconds
        def date_to_utc(date_obj):
            if date_obj:
                # Combine the date with midnight time to create a datetime object
                dt = datetime.datetime.combine(date_obj, datetime.time.min)
                # Make the datetime object timezone-aware in UTC using datetime.timezone.utc
                dt = timezone.make_aware(dt, datetime.timezone.utc)
                # Return timestamp in milliseconds
                return int(dt.timestamp()) * 1000
            return None

        # Collect all events with their start_date and end_date
        events = []

        # Add Country event if it has both start and end dates
        if country.start_date:
            events.append({
                'name': f"Country: {country.name}",
                'unique_id': country.id,
                'model_type': 'country',
                'start': date_to_utc(country.start_date),
                'end': date_to_utc(country.end_date) if country.end_date else current_timestamp,
                'level': 0,
                'color': '#4CAF50'
            })

        # Helper function to add events
        def add_events(items, level, color, label_prefix, model_type):
            for item in items:
                if item.start_date:
                    events.append({
                        'name': f"{label_prefix}: {item.name}",
                        'unique_id': item.id,
                        'model_type': model_type,
                        'start': date_to_utc(item.start_date),
                        'end': date_to_utc(item.end_date) if item.end_date else current_timestamp,
                        'level': level,
                        'color': color
                    })
                else:
                    logger.warning(f"Skipping {label_prefix} '{item.name}' because it lacks a valid start date.")

        # Add Historical Periods, Entities, and Currencies
        add_events(historical_periods, 1, '#2196F3', 'Historical Period', 'historicalperiod')
        add_events(entities, 2, '#FFC107', 'Entity', 'entity')
        add_events(currencies, 3, '#E91E63', 'Currency', 'currency')

        if not events:
            return [], []

        # Sort events by start date and assign unique y index
        events.sort(key=lambda x: x['start'])
        categories = [event['name'] for event in events]
        category_indices = {category: index for index, category in enumerate(categories)}

        # Assign y index to events
        for event in events:
            event['y'] = category_indices[event['name']]

        return events, categories


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'classification', 'start_date', 'end_date')
    search_fields = ('name', 'country__name', 'classification__type')
    list_filter = ('country', 'classification')
    inlines = [CurrencyInline]