from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountsSerializer, MembershipSerializer
from .models import Account

from utils.ctm import CTMAPI
from utils.permissions import hasReportManagerAccessLevel
from users.roles import *


class AccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    model = Account
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        profile = self.request.user.profile
        return profile.account_set.all() if not profile.agency_admin else Account.objects.all()


class AvailableAdminAccountsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        profile = request.user.profile
        response = MembershipSerializer(instance=profile.membership_set.all(), many=True).data\
            if profile.agency_admin \
            else MembershipSerializer(profile.membership_set.filter(role=ADMIN_ROLE),
                                      many=True).data

        return Response(response)


class AccountSourcesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, account_id=None):
        ctm_api = CTMAPI()
        response = ctm_api.get_sources(account_id)
        return Response(response)


class AccountReportsView(APIView):
    permission_classes = (IsAuthenticated, hasReportManagerAccessLevel)

    def get(self, request, account_id=None):
        ctm_api = CTMAPI()
        queryparams = request.GET
        response = ctm_api.get_calls_report(account_id, queryparams)
        return Response(response)
