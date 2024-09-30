
from django.db import models


from django.db import models

class Language(models.Model):
    iso_name = models.CharField(max_length=100, unique=True)
    iso2 = models.CharField(max_length=2, unique=True, null=True, blank=True)
    iso3 = models.CharField(max_length=3, unique=True, null=True, blank=True)
    native_name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"
        ordering = ['iso_name']

    def __str__(self):
        return self.iso_name

class AlternativeName(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='alternative_names')
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Alternative Name"
        verbose_name_plural = "Alternative Names"
        ordering = ['name']

    def __str__(self):
        return self.name









class Country(models.Model):
    iso_name = models.CharField(max_length=100, unique=True)
    official_state_name = models.CharField(max_length=100, unique=True)
    iso2 = models.CharField(max_length=2, unique=True, null=True, blank=True)
    iso3 = models.CharField(max_length=3, unique=True, null=True, blank=True)
    native_names = models.TextField(blank=True, null=True)
    alternative_names = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ['iso_name']

    def __str__(self):
        return self.iso_name

class CountryLanguage(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Country Language"
        verbose_name_plural = "Country Languages"
        ordering = ['country']

    def __str__(self):
        return f"{self.country} - {self.language}"

