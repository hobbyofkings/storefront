from django.db import models

# Create your models here.
from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)  # ISO language code, e.g., 'en', 'fr'
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"
        ordering = ['name']

    def __str__(self):
        return self.name