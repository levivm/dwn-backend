from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from utils.ctm import CTMAPI
from rest_framework.response import Response


class FindNumbersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, account_id=None):
        queryparams = request.GET
        ctm_api = CTMAPI()
        response = ctm_api.get_numbers(
            account_id,
            queryparams
        )
        return Response(response)


class ReceivingNumbersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, account_id=None):
        queryparams = request.GET
        ctm_api = CTMAPI()
        response = ctm_api.get_receiving_numbers(
            account_id,
            query_params=queryparams
        )
        return Response(response)


class TrackingNumbersView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, account_id=None):
        numbers = request.data.get(
            'numbers',
            []
        )
        ctm_api = CTMAPI()
        response = ctm_api.buy_numbers(
            account_id,
            numbers
        )
        return Response(response)

    def put(self, request, account_id=None):
        data = request.data
        ctm_api = CTMAPI()
        response = ctm_api.update_tracking_number(
            account_id,
            data
        )
        return Response(response)


class TrackingNumbersRoutesView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, account_id=None, tracking_number_id=None):
        data = request.data
        ctm_api = CTMAPI()
        response = ctm_api.update_tracking_number_routes(
            account_id,
            tracking_number_id,
            data
        )
        return Response(response)
