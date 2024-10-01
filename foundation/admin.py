from django.db import transaction, IntegrityError
from django.contrib import admin
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
    list_display = ('name', 'start_year', 'end_year', 'get_countries', 'get_currency_periods', 'created_at')
    search_fields = ('name',)
    list_filter = ('start_year', 'end_year')
    inlines = [CountryPeriodInline, CurrencyPeriodInline]

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
