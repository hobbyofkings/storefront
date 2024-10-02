from django.db import transaction, IntegrityError
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Language, AlternativeName, Country, CountryLanguage, Period, CurrencyPeriod, CountryPeriod, Demonym
from django.core.cache import cache
from django import forms

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
    readonly_fields = ['get_iso2', 'get_iso3', 'get_native_name']
    max_num = 5  # Limit to 5 inline rows


    # Use select_related to optimize queries for ForeignKey fields
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('language', 'country')
        return queryset

    def get_period_start_year(self, obj):
        return obj.period.start_year

    get_period_start_year.short_description = 'Start Year'

    def get_period_end_year(self, obj):
        return obj.period.end_year

    get_period_end_year.short_description = 'End Year'

    def get_currency_periods(self, obj):
        return ", ".join(
            [f"{cp.name} ({cp.start_year} - {cp.end_year or 'present'})" for cp in obj.period.currency_periods.all()])

    get_currency_periods.short_description = 'Currency Periods'

    def get_iso2(self, obj):
        return obj.language.iso2

    get_iso2.short_description = 'ISO2'

    def get_iso3(self, obj):
        return obj.language.iso3

    get_iso3.short_description = 'ISO3'

    def get_native_name(self, obj):
        return obj.language.native_name

    get_native_name.short_description = 'Native Name'





class CountryPeriodInline(admin.TabularInline):
    model = CountryPeriod
    extra = 1
    can_delete = True
    readonly_fields = ['get_period_name', 'get_period_start_year', 'get_period_end_year', 'get_currency_periods']


    # Use select_related to optimize queries for ForeignKey fields
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('country', 'period')
        return queryset

    def get_period_name(self, obj):
        return obj.period.name

    get_period_name.short_description = 'Period Name'

    def get_period_start_year(self, obj):
        return obj.period.start_year

    get_period_start_year.short_description = 'Start Year'

    def get_period_end_year(self, obj):
        return obj.period.end_year

    get_period_end_year.short_description = 'End Year'

    def get_currency_periods(self, obj):
        # Show detailed information for each currency period (name, start year, end year)
        return ", ".join(
            [f"{cp.name} ({cp.start_year} - {cp.end_year or 'present'})" for cp in obj.period.currency_periods.all()])

    get_currency_periods.short_description = 'Currency Periods'

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

# @admin.register(Demonym)
# class DemonymAdmin(admin.ModelAdmin):
#     form = DemonymAdminForm

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    form = CountryAdminForm
    list_display = ['flag_thumbnail_list', 'clickable_country_name', 'official_state_name', 'iso2', 'iso3', 'get_demonyms', 'get_languages', 'get_periods', 'created_at']
    search_fields = ['iso_name', 'official_state_name', 'iso2', 'iso3']
    list_filter = ['created_at']
    ordering = ['iso_name']
    inlines = [CountryLanguageInline, DemonymInline, CountryPeriodInline]
    readonly_fields = ('flag_thumbnail',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related(
            'countrylanguage_set__language',
            'countryperiod_set__period__currency_periods',
            # Be mindful of depth here; try removing currency_periods if too many queries
            'demonyms'
        )
        return queryset

    def get_languages(self, obj):
        # Use prefetch_related to get all related languages and avoid multiple queries
        return ", ".join([cl.language.name for cl in obj.countrylanguage_set.all()])
    get_languages.short_description = 'Languages'

    def get_periods(self, obj):
        cache_key = f"country_{obj.id}_periods"
        periods = cache.get(cache_key)
        if not periods:
            periods = ", ".join([cp.period.name for cp in obj.countryperiod_set.all()])
            cache.set(cache_key, periods, timeout=60 * 60)  # Cache for 1 hour
        return periods

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