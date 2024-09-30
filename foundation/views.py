from rest_framework import generics
from .models import Language
from .serializers import LanguageSerializer

class LanguageListView(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer