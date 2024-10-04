from django.core.files.base import ContentFile
from django.db import models
from django.utils.html import format_html
from django.db import models
from django.utils.html import format_html
from PIL import Image
import boto3
from django.conf import settings
import os
import io

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



class Continent(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Continent"
        verbose_name_plural = "Continents"
        ordering = ['name']

    def __str__(self):
        return self.name





class Country(models.Model):
    CONTINENT_CHOICES = [
        ('AF', 'Africa'),
        ('AN', 'Antarctica'),
        ('AS', 'Asia'),
        ('EU', 'Europe'),
        ('NA', 'North America'),
        ('OC', 'Oceania'),
        ('SA', 'South America'),
    ]
    iso_name = models.CharField(max_length=100, unique=True, help_text="ISO name of the country (e.g., United States, United Kingdom)")
    official_state_name = models.CharField(max_length=100, unique=False, null=True, blank=True, help_text="Official name of the country (e.g., United States of America, United Kingdom of Great Britain and Northern Ireland)")
    iso2 = models.CharField(max_length=2, unique=True, null=True, blank=True)
    iso3 = models.CharField(max_length=3, unique=True, null=True, blank=True)
    native_names = models.TextField(blank=True, null=True, help_text="Native names of the country (e.g., Deutschland, Россия)")
    alternative_names = models.TextField(blank=True, null=True, help_text="Alternative names for the country (e.g., 'USA', 'UK')")
    periods = models.ManyToManyField('Period', through='CountryPeriod', related_name='countries_related', blank=True)
    continent = models.CharField(max_length=2, choices=CONTINENT_CHOICES, help_text="Continent of the country", null=True, blank=True)
    country_start_year = models.IntegerField(null=True, blank=True, help_text="Year the country was established")
    country_end_year = models.IntegerField(null=True, blank=True, help_text="Year the country was dissolved")
    flag = models.ImageField(
        upload_to='flags/',
        blank=True,
        null=True,
        help_text="Flag of the country"
    )


    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ['iso_name']

    def __str__(self):
        return self.iso_name

    def save(self, *args, **kwargs):
        if self.flag:
            print("Flag detected, starting resizing process...")  # Debug statement
            img = Image.open(self.flag)

            print(f"Original image size: {img.size}")  # Debug statement

            # Resize image to 50 width, maintaining aspect ratio
            width = 50
            aspect_ratio = img.height / img.width
            height = int(width * aspect_ratio)
            img = img.resize((width, height), Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS

            print(f"Resized image size: {img.size}")  # Debug statement

            # Save the resized image in memory
            img_io = io.BytesIO()
            img_format = 'PNG' if self.flag.name.lower().endswith('.png') else 'JPEG'
            img.save(img_io, format=img_format)
            img_content = ContentFile(img_io.getvalue(), name=self.flag.name)

            # Update the image field with the resized image
            self.flag = img_content

        super().save(*args, **kwargs)

    def __str__(self):
        return self.iso_name

    def country_flag_thumbnail(self):
        if self.flag:
            return format_html('<img src="{}" width="50px" />', self.flag.url)
        return "-"

    country_flag_thumbnail.short_description = "Flag Thumbnail"



class CountryLanguage(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Country Language"
        verbose_name_plural = "Country Languages"
        ordering = ['country']
        indexes = [
            models.Index(fields=['country']),
            models.Index(fields=['language']),
            models.Index(fields=['country', 'language']),  # Composite index for faster lookups
        ]

    def __str__(self):
        return f"{self.country} - {self.language}"


class Period(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Name of the historical or numismatic period (e.g., Third Reich, Late Soviet Union)")
    alternative_names = models.TextField(blank=True, null=True, help_text="Alternative names for the period (e.g., 'Nazis', 'USSR')")
    description = models.TextField(blank=True, null=True, help_text="Description of the period")
    coat_of_arms = models.ImageField(
        upload_to='periods/',
        blank=True,
        null=True,
        help_text="Coat of arms or emblem of the period"
    )
    start_year = models.IntegerField(null=True, blank=True, help_text="Year the period started (optional)")
    end_year = models.IntegerField(null=True, blank=True, help_text="Year the period ended (optional)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Period"
        verbose_name_plural = "Periods"
        ordering = ['name']

    def __str__(self):
        return self.name

    def coat_of_arms_thumbnail(self):
        if self.coat_of_arms:
            return format_html('<img src="{}" width="200px" />', self.coat_of_arms.url)
        return "-"

    coat_of_arms_thumbnail.short_description = "Coat of Arms Thumbnail"


class CountryPeriod(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    period = models.ForeignKey('Period', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Country Period"
        verbose_name_plural = "Country Periods"
        unique_together = ('country', 'period')

    def __str__(self):
        return f"{self.country} - {self.period}"

# class CurrencyPeriod(models.Model):
#     period = models.ForeignKey(Period, related_name='currency_periods', on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=100, help_text="Name of the currency period (e.g., Deutsche Mark, Euro)")
#     alternative_names = models.TextField(blank=True, null=True, help_text="Alternative names for the currency period")
#     start_year = models.IntegerField(help_text="Year the currency period started")
#     end_year = models.IntegerField(null=True, blank=True, help_text="Year the currency period ended (leave blank if ongoing)")
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         verbose_name = "Currency Period"
#         verbose_name_plural = "Currency Periods"
#         ordering = ['period', 'start_year']
#
#     def __str__(self):
#         return f"{self.name} ({self.start_year}-{self.end_year or 'present'})"












class Demonym(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='demonyms', help_text='Associated country')
    # language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True, related_name='demonyms', help_text='Associated language (optional)')
    main_demonym = models.CharField(max_length=255, null=True, blank=True, unique=True, help_text='Demonym in English')
    alternative_demonyms = models.TextField(blank=True, null=True,
                                            help_text='Array of alternative demonym forms (e.g., adjectives in other languages)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Demonym"
        verbose_name_plural = "Demonyms"
        ordering = ['country', 'main_demonym']  # Updated ordering field

    def __str__(self):
        return self.main_demonym  # Updated to use the correct field name





class HistoricalPeriod(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='historical_periods')
    name = models.CharField(max_length=100, unique=True, help_text="Name of the historical period")
    start_year = models.IntegerField(null=True, blank=True, help_text="Year the period started (optional)")
    end_year = models.IntegerField(null=True, blank=True, help_text="Year the period ended (optional)")
    description = models.TextField(blank=True, null=True, help_text="Description of the period")
    coat_of_arms = models.ImageField(upload_to='periods/', blank=True, null=True, help_text="Coat of arms or emblem of the period")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historical Period"
        verbose_name_plural = "Historical Periods"
        ordering = ['name']

    def __str__(self):
        return self.name

    def coat_of_arms_thumbnail(self):
        if self.coat_of_arms:
            return format_html('<img src="{}" width="200px" />', self.coat_of_arms.url)
        return "-"

    coat_of_arms_thumbnail.short_description = "Coat of Arms Thumbnail"

class AdministrativeUnitType(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Name of the administrative unit type (e.g., State, Territory)")

    class Meta:
        verbose_name = "Administrative Unit Type"
        verbose_name_plural = "Administrative Unit Types"
        ordering = ['name']

    def __str__(self):
        return self.name

class AdministrativeUnit(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='administrative_units')
    name = models.CharField(max_length=100, unique=False, help_text="Name of the administrative unit")
    type = models.ForeignKey(AdministrativeUnitType, on_delete=models.SET_NULL, null=True, blank=True, help_text="Type of administrative unit (e.g., state, territory)")

    start_year = models.IntegerField(null=True, blank=True, help_text="Year the administrative unit was established")
    end_year = models.IntegerField(null=True, blank=True, help_text="Year the administrative unit was dissolved")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Administrative Unit"
        verbose_name_plural = "Administrative Units"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.type})"


class CurrencyPeriod(models.Model):
    COLLECTIBLE_TYPES = [
        ('coin', 'Coin'),
        ('banknote', 'Banknote'),
        ('stamp', 'Postage Stamp'),
    ]

    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE, related_name='currency_periods', null=True, blank=True)
    historical_period = models.ForeignKey(HistoricalPeriod, on_delete=models.CASCADE, related_name='currency_periods', null=True, blank=True)
    name = models.CharField(max_length=100, help_text="Name of the currency period (e.g., Deutsche Mark, Euro)")
    # type = models.CharField(max_length=50, help_text="Type of currency (e.g., coin, banknote)", default='coin')
    type = models.CharField(
        max_length=20,
        choices=COLLECTIBLE_TYPES,
        help_text="Type of currency (e.g., coin, banknote)",
        default='coin'
    )


    start_year = models.IntegerField(help_text="Year the currency period started")
    end_year = models.IntegerField(null=True, blank=True, help_text="Year the currency period ended (leave blank if ongoing)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Currency Period"
        verbose_name_plural = "Currency Periods"
        ordering = ['start_year']

    def __str__(self):
        return f"{self.name} ({self.start_year}-{self.end_year or 'present'})"


class Currency(models.Model):
    currency_period = models.ForeignKey(CurrencyPeriod, on_delete=models.CASCADE, related_name='currencies')
    name = models.CharField(max_length=100, help_text="Name of the currency (e.g., Mark, Euro)")
    denomination = models.DecimalField(max_digits=10, decimal_places=2, help_text="Denomination of the currency")
    issue_date = models.DateField(help_text="Date the currency was issued")
    type = models.CharField(max_length=50, help_text="Type of currency (e.g., coin, banknote)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.denomination} ({self.issue_date})"





