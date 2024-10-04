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




class YearField(forms.Field):
    def to_python(self, value):
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            raise forms.ValidationError('Enter a valid year.')

    def validate(self, value):
        super().validate(value)
        if value and (value < 1 or value > datetime.date.today().year):
            raise forms.ValidationError('Enter a valid year.')

def validate_year(value):
    current_year = timezone.now().year
    if value < 0 or value > current_year:
        raise ValidationError(f"Enter a valid year between 0 and {current_year}.")


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
    continent = models.CharField(max_length=2, choices=CONTINENT_CHOICES, help_text="Continent of the country", null=True, blank=True)

    country_start_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[validate_year],
        help_text="Year the country was established"
    )
    country_end_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[validate_year],
        help_text="Year the country was dissolved"
    )




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



class CountryGroup(models.Model):
    name = models.CharField(max_length=255)
    start_date =  models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[validate_year],
        help_text="Year the country group was established"
    )
    end_date = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[validate_year],
        help_text="Year the country group was dissolved"
    )

    class Meta:
        verbose_name = "Country Group"
        verbose_name_plural = "Country Groups"
        ordering = ['name']

    def __str__(self):
        return self.name


class CountryGroupMember(models.Model):
    country_group = models.ForeignKey(
        CountryGroup,
        on_delete=models.CASCADE,
        related_name='members',
        help_text="Associated country group"
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='country_groups',
        help_text="Associated country"
    )

    class Meta:
        verbose_name = "Country Group Member"
        verbose_name_plural = "Country Group Members"
        unique_together = ('country_group', 'country')
        ordering = ['country_group', 'country']

    def __str__(self):
        return f"{self.country} in {self.country_group}"


# class EntityType(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#
#     class Meta:
#         verbose_name = "Entity Type"
#         verbose_name_plural = "Entity Types"
#         ordering = ['name']
#
#     def __str__(self):
#         return self.name

class EntityType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ParentEntity(models.Model):
    name = models.CharField(max_length=255)
    entity_type = models.ForeignKey('EntityType', on_delete=models.CASCADE)

    start_date = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[validate_year],
        help_text="Year the parent entity was established"
    )
    end_date = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[validate_year],
        help_text="Year the parent entity was dissolved"
    )

    class Meta:
        verbose_name = "Parent Entity"
        verbose_name_plural = "Parent Entities"
        ordering = ['name']

    def __str__(self):
        return self.name


class ParentEntityCountry(models.Model):
    parent_entity = models.ForeignKey(
        ParentEntity,
        on_delete=models.CASCADE,
        related_name='parent_entity_countries',
        help_text="Associated parent entity"
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='parent_entity_countries_countries',  # Changed to be unique
        help_text="Associated country"
    )
    country_group = models.ForeignKey(
        CountryGroup,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='parent_entity_country_groups',  # Changed to be unique
        help_text="Associated country group (optional)"
    )

    class Meta:
        verbose_name = "Parent Entity Country"
        verbose_name_plural = "Parent Entity Countries"
        unique_together = ('parent_entity', 'country')

    def __str__(self):
        return f"{self.country} under {self.parent_entity}"

# class SovereignStatus(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#
#     class Meta:
#         verbose_name = "Sovereign Status"
#         verbose_name_plural = "Sovereign Statuses"
#         ordering = ['name']
#
#     def __str__(self):
#         return self.name


class SovereignStatus(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Entity(models.Model):
    parent_entity = models.ForeignKey(
        ParentEntity,
        on_delete=models.CASCADE,
        related_name='entities',
        help_text="Parent entity"
    )
    sovereign_status = models.ForeignKey('SovereignStatus', on_delete=models.CASCADE)
    entity_type = models.ForeignKey('EntityType', on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    start_date = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[validate_year],
        help_text="Year the entity was established"
    )
    end_date = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[validate_year],
        help_text="Year the entity was dissolved"
    )

    class Meta:
        verbose_name = "Entity"
        verbose_name_plural = "Entities"
        ordering = ['name']

    def __str__(self):
        return self.name



class HistoricalPeriod(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[validate_year],
        help_text="Start year of the historical period"
    )
    end_date = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[validate_year],
        help_text="End year of the historical period"
    )

    entities = models.ManyToManyField(
        Entity,
        through='EntityHistoricalPeriod',
        related_name='historical_periods',  # Changed to avoid redundancy and confusion
    )

    class Meta:
        verbose_name = "Historical Period"
        verbose_name_plural = "Historical Periods"
        ordering = ['start_date', 'name']

    def __str__(self):
        return self.name

    def get_entities(self):
        return Entity.objects.filter(
            entityhistoricalperiod__historical_period=self
        ).distinct()




class EntityHistoricalPeriod(models.Model):
    entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name='historical_period_links',  # For accessing historical periods from an entity
        help_text="Associated entity",
    )
    historical_period = models.ForeignKey(
        HistoricalPeriod,
        on_delete=models.CASCADE,
        related_name='entity_historical_period_links',  # For accessing entities from a historical period
        help_text="Associated historical period",
    )

    class Meta:
        verbose_name = "Entity Historical Period"
        verbose_name_plural = "Entity Historical Periods"
        unique_together = ("entity", "historical_period")
        ordering = ["entity", "historical_period"]

    def __str__(self):
        return f"{self.entity} during {self.historical_period}"

# class CurrencyType(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#
#     class Meta:
#         verbose_name = "Currency Type"
#         verbose_name_plural = "Currency Types"
#         ordering = ['name']
#
#     def __str__(self):
#         return self.name


class CurrencyType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name




# class IssuanceReason(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#
#     class Meta:
#         verbose_name = "Issuance Reason"
#         verbose_name_plural = "Issuance Reasons"
#         ordering = ['name']
#
#     def __str__(self):
#         return self.name


class IssuanceReason(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name




class Currency(models.Model):

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='currencies')
    currency_type = models.ForeignKey(CurrencyType, on_delete=models.CASCADE)
    issuance_reason = models.ForeignKey(IssuanceReason, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)





    start_date = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[validate_year],
        help_text="Year the currency was introduced"
    )
    end_date = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[validate_year],
        help_text="Year the currency was discontinued"
    )
    denominations = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Denominations of the currency"
    )
    notes = models.TextField(null=True, blank=True, help_text="Additional notes about the currency")

    # class Meta:
    #     verbose_name = "Currency"
    #     verbose_name_plural = "Currencies"
    #     ordering = ['name']

    def __str__(self):
        return self.name

class CurrencyForm(forms.ModelForm):
    start_date = YearField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'YYYY'}),
        help_text="Year the currency was introduced"
    )
    end_date = YearField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'YYYY'}),
        help_text="Year the currency was discontinued"
    )

    class Meta:
        model = Currency
        fields = '__all__'

    def clean_start_date(self):
        year = self.cleaned_data['start_date']
        if year:
            return datetime.date(year, 1, 1)
        return None

    def clean_end_date(self):
        year = self.cleaned_data['end_date']
        if year:
            return datetime.date(year, 12, 31)
