from django.db import models




class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    iso2 = models.CharField(max_length=2, unique=True, null=True, blank=True)
    iso3 = models.CharField(max_length=3, unique=True, null=True, blank=True)
    native_name = models.CharField(max_length=100, unique=True, null=True, blank=True, help_text="Name of the language in its native script")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"
        ordering = ['name']

    def __str__(self):
        return self.name

class AlternativeName(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='alternative_names')
    name = models.CharField(max_length=255, unique=True, help_text="Alternative name for the language")

    class Meta:
        verbose_name = "Alternative Name"
        verbose_name_plural = "Alternative Names"
        ordering = ['name']

    def __str__(self):
        return self.name









class Country(models.Model):
    iso_name = models.CharField(max_length=100, unique=True, help_text="ISO name of the country (e.g., United States, United Kingdom)")
    official_state_name = models.CharField(max_length=100, unique=False, null=True, blank=True, help_text="Official name of the country (e.g., United States of America, United Kingdom of Great Britain and Northern Ireland)")
    iso2 = models.CharField(max_length=2, unique=True, null=True, blank=True)
    iso3 = models.CharField(max_length=3, unique=True, null=True, blank=True)
    native_names = models.TextField(blank=True, null=True, help_text="Native names of the country (e.g., Deutschland, Россия)")
    alternative_names = models.TextField(blank=True, null=True, help_text="Alternative names for the country (e.g., 'USA', 'UK')")
    periods = models.ManyToManyField('Period', through='CountryPeriod', related_name='countries_related', blank=True, help_text="Historical periods associated with the country")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ['iso_name']

    def __str__(self):
        return self.iso_name

class CountryLanguage(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Country Language"
        verbose_name_plural = "Country Languages"
        ordering = ['country']

    def __str__(self):
        return f"{self.country} - {self.language}"


class Period(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            help_text="Name of the numismatic / historical period (e.g., Third Reich, Late Soviet Union)")
    alternative_names = models.TextField(blank=True, null=True, help_text="Alternative names for the period (e.g., 'Nazis', 'USSR')")
    start_year = models.IntegerField(null=True, blank=True, help_text="Year the period started (optional)")
    end_year = models.IntegerField(null=True, blank=True, help_text="Year the period ended (optional)")
    countries = models.ManyToManyField(Country, through='CountryPeriod', related_name='periods_related', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Period"
        verbose_name_plural = "Periods"
        ordering = ['name']

    def __str__(self):
        return self.name


class CountryPeriod(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Country Period"
        verbose_name_plural = "Country Periods"
        unique_together = ('country', 'period')

    def __str__(self):
        return f"{self.country} - {self.period}"