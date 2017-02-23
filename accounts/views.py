from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AccountsSerializer, MembershipSerializer
from .models import Account

from utils.ctm import CTMAPI


from users.roles import *


class AccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    model = Account

    def get_queryset(self):
        profile = self.request.user.profile
        return profile.account_set.all()


class AvailableAdminAccountsView(APIView):

    def get(self, request):
        profile = request.user.profile
        response = MembershipSerializer(instance=profile.membership_set.all(), many=True).data\
            if profile.agency_admin \
            else MembershipSerializer(profile.membership_set.filter(role=ADMIN_ROLE),
                                      many=True).data

        return Response(response)


class AccountSourcesView(APIView):

    def get(self, request, account_id=None):
        ctm_api = CTMAPI()
        response = ctm_api.get_sources(account_id)
        return Response(response)
