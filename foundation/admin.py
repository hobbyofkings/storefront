from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Language  # Replace Language with your model name if different

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Replace with fields in your model