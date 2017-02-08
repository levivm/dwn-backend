from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.ctm import CTMAPI

from .serializers import AccountsSerializer
from .models import Account
# Create your views here.


class AccountsViewSet(viewsets.ModelViewSet):
    serializer_class = AccountsSerializer
    model = Account

    def get_queryset(self):
        profile = self.request.user.profile
        return profile.account_set.all()


class AccountCalls(APIView):

    def get(self, request, account_id=None):
        page = request.GET.get('page', 1)
        ctm_api = CTMAPI()
        response = ctm_api.get_calls(account_id, page)
        return Response(response)

    def post(self, request, account_id=None, call_id=None):
        data = request.data
        print(data)
        ctm_api = CTMAPI()
        response = ctm_api.update_call(account_id, call_id, data)
        return Response(response)
