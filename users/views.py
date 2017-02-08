from django.shortcuts import render
from rest_framework import viewsets

from .serializers import ProfilesSerializer
from .models import Profile

# Create your views here.


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfilesSerializer
    queryset = Profile.objects.all()
    model = Profile
