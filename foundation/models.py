from datetime import datetime
from django import forms
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
from django.core.exceptions import ValidationError
from django.utils import timezone




class EntityClassification(models.Model):
    type = models.CharField(max_length=255)  # e.g., Kingdom, State, City
    sovereignty = models.CharField(max_length=255)  # e.g., Sovereign State, Semi-Sovereign, Autonomous

    def __str__(self):
        return f"{self.type} ({self.sovereignty})"




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
    name = models.CharField(max_length=100, unique=True, help_text="ISO name of the country (e.g., United States, United Kingdom). A Country represents a sovereign state—an independent nation with defined borders, a permanent population, a government, and the capacity to enter into relations with other states. Countries can span various historical periods, maintaining continuity despite changes in governance, leadership, or political systems.")
    # official_state_name = models.CharField(max_length=100, unique=False, null=True, blank=True, help_text="Official name of the country (e.g., United States of America, United Kingdom of Great Britain and Northern Ireland)")
    iso2 = models.CharField(max_length=2, unique=True, null=True, blank=True)
    iso3 = models.CharField(max_length=3, unique=True, null=True, blank=True)
    native_names = models.TextField(blank=True, null=True, help_text="Native names of the country (e.g., Deutschland, Россия)")
    alternative_names = models.TextField(blank=True, null=True, help_text="Alternative names for the country (e.g., 'USA', 'UK')")
    # continent = models.CharField(max_length=2, choices=CONTINENT_CHOICES, help_text="Continent of the country", null=True, blank=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, related_name='countries')

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)




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
        ordering = ['name']

    def __str__(self):
        return self.name

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


class SovereignStatus(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Entity(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='entities', help_text='An Entity refers to a subnational division or historical administrative unit within a country. Entities can vary in their degree of autonomy and governance structure. They can be provinces, states, kingdoms, duchies, cities, or other administrative regions.')
    classification = models.ForeignKey(EntityClassification, on_delete=models.CASCADE, related_name='entities')
    name = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class HistoricalPeriod(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='historical_periods')
    name = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.country.name})"








class Currency(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='currencies')
    currency_type = models.CharField(max_length=255)  # e.g., Coin, Banknote
    name = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    denominations = models.CharField(max_length=255, blank=True)  # e.g., "1 Mark, 5 Mark"
    issuance_reason = models.TextField(blank=True)  # e.g., "War Effort"
    historical_context = models.TextField(blank=True)  # e.g., "Impact of WWI"

    def __str__(self):
        return self.name


