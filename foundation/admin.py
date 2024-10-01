from django.db import transaction, IntegrityError
from django.contrib import admin
from django.utils.html import format_html

from .models import Language, AlternativeName, Country, CountryLanguage, Period, CurrencyPeriod, CountryPeriod


# Inline for managing alternative names of a language
class AlternativeNameInline(admin.TabularInline):
    model = AlternativeName
    extra = 1
    can_delete = True


# Inline for managing relationships between countries and languages
class CountryLanguageInline(admin.TabularInline):
    model = CountryLanguage
    extra = 1
    can_delete = True

class CountryPeriodInline(admin.TabularInline):
    model = CountryPeriod
    extra = 1
    can_delete = True

class CurrencyPeriodInline(admin.TabularInline):
    model = CurrencyPeriod
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


# Admin for managing Country with inline for language relationships
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['iso_name', 'official_state_name', 'iso2', 'iso3', 'created_at']
    search_fields = ['iso_name', 'official_state_name', 'iso2', 'iso3']
    list_filter = ['created_at']
    ordering = ['iso_name']
    inlines = [CountryLanguageInline, CountryPeriodInline]  # Add inlines for managing country-language, country-period, and currency-period relationships




# @admin.register(Period)
# class PeriodAdmin(admin.ModelAdmin):
#     list_display = ('name', 'start_year', 'end_year', 'get_countries', 'get_currency_periods', 'created_at')
#     search_fields = ('name',)
#     list_filter = ('start_year', 'end_year')
#     inlines = [CountryPeriodInline, CurrencyPeriodInline]
#
#     def get_countries(self, obj):
#         """Returns a comma-separated list of countries related to the period."""
#         return ", ".join([country.iso_name for country in obj.countries_related.all()])
#
#     get_countries.short_description = 'Countries'
#
#     def get_currency_periods(self, obj):
#         """Returns a comma-separated list of currency periods related to the period."""
#         return ", ".join([currency_period.name for currency_period in obj.currency_periods.all()])
#
#     get_currency_periods.short_description = 'Currency Periods'


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_year', 'end_year', 'get_countries', 'get_currency_periods', 'coat_of_arms_list_thumbnail', 'created_at')
    search_fields = ('name',)
    list_filter = ('start_year', 'end_year')
    inlines = [CountryPeriodInline, CurrencyPeriodInline]
    # readonly_fields = ('coat_of_arms_thumbnail',)
    fields = ['name', 'alternative_names', 'description', 'coat_of_arms', 'coat_of_arms_thumbnail', 'start_year', 'end_year']


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Prefetch countries and currency periods for efficiency
        queryset = queryset.prefetch_related('countries_related', 'currency_periods')
        return queryset

    def get_countries(self, obj):
        return ", ".join([country.iso_name for country in obj.countries_related.all()])
    get_countries.short_description = 'Countries'

    def get_currency_periods(self, obj):
        return ", ".join([currency_period.name for currency_period in obj.currency_periods.all()])
    get_currency_periods.short_description = 'Currency Periods'

    def get_readonly_fields(self, request, obj=None):
        # Add 'coat_of_arms_thumbnail' as a readonly field if editing an existing object
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj:  # Only add the thumbnail for existing objects
            readonly_fields.append('coat_of_arms_thumbnail')
        return readonly_fields

    def coat_of_arms_thumbnail(self, obj):
        # Display the thumbnail of the coat of arms
        if obj.coat_of_arms:
            return format_html('<img src="{}" width="200" height="auto" />', obj.coat_of_arms.url)
        return "No image available"
    coat_of_arms_thumbnail.short_description = "Coat of Arms Thumbnail"

    def coat_of_arms_list_thumbnail(self, obj):
        # Display a smaller version of the coat of arms in the list view
        if obj.coat_of_arms:
            return format_html('<img src="{}" width="50" height="auto" />', obj.coat_of_arms.url)
        return "No image available"
    coat_of_arms_list_thumbnail.short_description = "Coat of Arms"