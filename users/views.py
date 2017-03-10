from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from utils.permissions import hasAdminAccessLevel

from .serializers import ProfilesSerializer
from .models import Profile
from .roles import ROLES_CHOICES, AGENCY_ADMIN, AGENCY_ADMIN_DISPLAY


# Create your views here.


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, hasAdminAccessLevel)
    serializer_class = ProfilesSerializer
    queryset = Profile.objects.all()
    model = Profile

    def get_queryset(self):
        request = self.request
        queryset = self.queryset
        account_id = request.parser_context\
            .get('kwargs', {}).get('account_id')
        queryset = Profile.objects.filter(membership__account__call_metrics_id=account_id)\
            if account_id else self.queryset
        return queryset


class UsersRolesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        roles = map(lambda role: {'name': role[0], 'value': role[1]}, ROLES_CHOICES)
        return Response(roles)
