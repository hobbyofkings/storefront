from django.db import transaction, IntegrityError
from django.contrib import admin
from django.utils.html import format_html

from .models import Language, AlternativeName, Country, CountryLanguage, Period, CurrencyPeriod, CountryPeriod, Demonym


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

    # Use select_related to optimize queries for ForeignKey fields
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('language', 'country')
        return queryset

class CountryPeriodInline(admin.TabularInline):
    model = CountryPeriod
    extra = 1
    can_delete = True

    # Use select_related to optimize queries for ForeignKey fields
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('country', 'period')
        return queryset


# Inline for managing relationships between demonyms and countries
class DemonymInline(admin.TabularInline):
    model = Demonym
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


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['iso_name', 'official_state_name', 'iso2', 'iso3', 'get_demonyms', 'get_languages', 'get_periods', 'flag_thumbnail_list', 'created_at']
    search_fields = ['iso_name', 'official_state_name', 'iso2', 'iso3']
    list_filter = ['created_at']
    ordering = ['iso_name']
    inlines = [CountryLanguageInline, DemonymInline, CountryPeriodInline]
    readonly_fields = ('flag_thumbnail',)



    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Use select_related and prefetch_related to reduce the number of queries
        queryset = queryset.prefetch_related('countrylanguage_set__language', 'countryperiod_set__period','demonyms')
        return queryset

    def get_languages(self, obj):
        # Use prefetch_related to get all related languages and avoid multiple queries
        return ", ".join([cl.language.name for cl in obj.countrylanguage_set.all()])
    get_languages.short_description = 'Languages'

    def get_periods(self, obj):
        # Use prefetch_related to get all related periods and avoid multiple queries
        return ", ".join([cp.period.name for cp in obj.countryperiod_set.all()])
    get_periods.short_description = 'Periods'

    def get_demonyms(self, obj):
        return ", ".join([demonym.main_demonym for demonym in obj.demonyms.all()])
    get_demonyms.short_description = 'Demonyms'

    def flag_thumbnail(self, obj):
        # Display a larger version of the flag on the detail page
        if obj.flag:
            return format_html('<img src="{}" width="200" height="auto" />', obj.flag.url)
        return "-"

    flag_thumbnail.short_description = "Flag Thumbnail"

    def flag_thumbnail_list(self, obj):
        # Display a smaller version of the flag in the list view
        if obj.flag:
            return format_html('<img src="{}" width="50" height="auto" />', obj.flag.url)
        return "-"

    flag_thumbnail_list.short_description = "Flag"






@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_year', 'end_year', 'get_countries', 'get_currency_periods', 'coat_of_arms_list_thumbnail', 'created_at')
    search_fields = ('name',)
    list_filter = ('start_year', 'end_year')
    inlines = [CountryPeriodInline, CurrencyPeriodInline]

    # Use this to include the thumbnail as a read-only field during editing
    readonly_fields = ('coat_of_arms_thumbnail',)

    fieldsets = (
        (None, {
            'fields': ('name', 'alternative_names', 'description', 'coat_of_arms', 'start_year', 'end_year', 'coat_of_arms_thumbnail'),
        }),
    )

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