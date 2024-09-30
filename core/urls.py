from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Root URL for the core app, serves the index view
]
