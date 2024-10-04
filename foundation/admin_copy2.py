
from django.db import transaction, IntegrityError
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Country,
    ParentEntity,
    Entity,
    EntityType,
    SovereignStatus,
    ParentEntityCountry,
    HistoricalPeriod,
    EntityHistoricalPeriod,
    Currency,
    CurrencyType,
    IssuanceReason,
    CountryGroup, AlternativeName, CountryGroupMember, Demonym, CountryLanguage, Language)

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


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_entity', 'sovereign_status', 'entity_type', 'start_date', 'end_date']
    search_fields = ['name']

class AlternativeNameInline(admin.TabularInline):
    model = AlternativeName
    extra = 1
    can_delete = True

@admin.register(CountryGroup)
class CountryGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date']
    search_fields = ['name']

@admin.register(CountryGroupMember)
class CountryGroupMemberAdmin(admin.ModelAdmin):
    list_display = ['country_group', 'country']
    search_fields = ['country_group__name', 'country__iso_name']


@admin.register(EntityType)
class EntityTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(ParentEntity)
class ParentEntityAdmin(admin.ModelAdmin):
    list_display = ['name', 'entity_type', 'start_date', 'end_date']
    search_fields = ['name']


@admin.register(ParentEntityCountry)
class ParentEntityCountryAdmin(admin.ModelAdmin):
    list_display = ['parent_entity', 'country', 'country_group']
    search_fields = ['parent_entity__name', 'country__iso_name']

@admin.register(SovereignStatus)
class SovereignStatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(HistoricalPeriod)
class HistoricalPeriodAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date']
    search_fields = ['name']


@admin.register(EntityHistoricalPeriod)
class EntityHistoricalPeriodAdmin(admin.ModelAdmin):
    list_display = ['entity', 'historical_period']
    search_fields = ['entity__name', 'historical_period__name']

@admin.register(CurrencyType)
class CurrencyTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(IssuanceReason)
class IssuanceReasonAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']








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
        'official_state_name',
        'iso2',
        'iso3',
        'get_languages',

        'continent',
        'country_start_year',
        'country_end_year',
        'created_at'
    ]
    search_fields = ['iso_name', 'official_state_name', 'iso2', 'iso3']
    list_filter = ['created_at']
    ordering = ['iso_name']
    inlines = [CountryLanguageInline, DemonymInline]

    readonly_fields = ('flag_thumbnail',)
    change_form_template = 'admin/foundation/country/change_form.html'


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related(
            'countrylanguage_set__language',
            'demonyms'
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
        return format_html('<a href="{}">{}</a>', url, obj.iso_name)
    clickable_country_name.short_description = 'Country Name'

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if not extra_context:
            extra_context = {}

        # Get the Country instance
        country = get_object_or_404(Country, pk=object_id)

        # Fetch related entities with the corrected filter
        entities = Entity.objects.filter(
            parent_entity__parent_entity_countries__country=country
        ).select_related(
            'parent_entity', 'sovereign_status', 'entity_type'
        ).prefetch_related(
            'historical_period_links__historical_period'
        ).distinct()

        # Fetch historical periods through EntityHistoricalPeriod using the correct related name
        historical_periods = HistoricalPeriod.objects.filter(
            entity_historical_period_links__entity__in=entities
        ).distinct()

        # Fetch currencies related to entities
        currencies = Currency.objects.filter(
            entity__in=entities
        ).select_related('currency_type', 'issuance_reason')

        # Debugging: Verify counts
        print(f"Entities Count: {entities.count()}")
        print(f"Historical Periods Count: {historical_periods.count()}")
        print(f"Currencies Count: {currencies.count()}")

        # Process data for the timeline
        timeline_data = self.prepare_timeline_data(country, entities, historical_periods, currencies)

        # Add the timeline data to the context
        extra_context['timeline_data'] = timeline_data
        extra_context['country'] = country

        return super().changeform_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def prepare_timeline_data(self, country, entities, historical_periods, currencies):
        timeline_data = []
        current_year = timezone.now().year  # Correct usage of Django's timezone

        # Helper function to convert year to a date string
        def year_to_date(year, month=1, day=1):
            if year:
                return f"{year}-{month:02d}-{day:02d}"
            return None

        # Add the country timeline
        timeline_data.append({
            'category': 'Country',
            'name': country.iso_name,
            'start': year_to_date(country.country_start_year),
            'end': year_to_date(country.country_end_year) if country.country_end_year else f"{current_year}-12-31",
        })

        # Add historical periods
        for period in historical_periods:
            print(f"Adding Historical Period: {period}")
            timeline_data.append({
                'category': 'Historical Periods',
                'name': period.name,
                'start': year_to_date(period.start_date),
                'end': year_to_date(period.end_date) if period.end_date else f"{current_year}-12-31",
            })

        # Add entities
        for entity in entities:
            print(f"Adding Entity: {entity}")
            timeline_data.append({
                'category': 'Entities',
                'name': entity.name,
                'start': year_to_date(entity.start_date),
                'end': year_to_date(entity.end_date) if entity.end_date else f"{current_year}-12-31",
            })

        # Add currencies
        for currency in currencies:
            print(f"Adding Currency: {currency}")
            timeline_data.append({
                'category': 'Currencies',
                'name': currency.name,
                'start': year_to_date(currency.start_date),
                'end': year_to_date(currency.end_date) if currency.end_date else f"{current_year}-12-31",
            })

        # Debugging: Print the timeline data
        print("Timeline Data:", timeline_data)

        return timeline_data

def prepare_timeline_data(self, country, entities, historical_periods, currencies):
    timeline_data = []
    current_year = timezone.now().year  # Correct usage of Django's timezone

    # Helper function to convert year to a date string
    def year_to_date(year, month=1, day=1):
        if year:
            return f"{year}-{month:02d}-{day:02d}"
        return None

    # Add the country timeline
    timeline_data.append({
        'category': 'Country',
        'name': country.iso_name,
        'start': year_to_date(country.country_start_year),
        'end': year_to_date(country.country_end_year) if country.country_end_year else f"{current_year}-12-31",
    })

    # Add historical periods
    for period in historical_periods:
        print(f"Adding Historical Period: {period}")
        timeline_data.append({
            'category': 'Historical Periods',
            'name': period.name,
            'start': year_to_date(period.start_date),
            'end': year_to_date(period.end_date) if period.end_date else f"{current_year}-12-31",
        })

    # Add entities
    for entity in entities:
        print(f"Adding Entity: {entity}")
        timeline_data.append({
            'category': 'Entities',
            'name': entity.name,
            'start': year_to_date(entity.start_date),
            'end': year_to_date(entity.end_date) if entity.end_date else f"{current_year}-12-31",
        })

    # Add currencies
    for currency in currencies:
        print(f"Adding Currency: {currency}")
        timeline_data.append({
            'category': 'Currencies',
            'name': currency.name,
            'start': year_to_date(currency.start_date),
            'end': year_to_date(currency.end_date) if currency.end_date else f"{current_year}-12-31",
        })

    # Debugging: Print the timeline data
    print("Timeline Data:", timeline_data)

    return timeline_data