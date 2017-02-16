from rest_framework.views import APIView
from rest_framework.response import Response

from utils.ctm import CTMAPI

from .dummy_data import DUMMY_RESPONSE


class CallsGetCreateView(APIView):

    def get(self, request, account_id=None):
        page = request.GET.get('page', 1)
        ctm_api = CTMAPI()
        # response = ctm_api.get_calls(account_id, page)
        return Response(DUMMY_RESPONSE)

    def post(self, request, account_id=None, call_id=None):
        data = request.data
        ctm_api = CTMAPI()
        response = ctm_api.update_call(account_id, call_id, data)
        return Response(response)


class CallsSaleUpdateView(APIView):

    def post(self, request, account_id=None, call_id=None):
        data = request.data
        ctm_api = CTMAPI()
        response = ctm_api.update_call_sale(account_id, call_id, data)
        return Response(response)
