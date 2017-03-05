from django.http import HttpResponse, StreamingHttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from utils.ctm import CTMAPI

from .dummy_data import DUMMY_RESPONSE


class CallsGetCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, account_id=None):
        page = request.GET.get('page', 1)
        ctm_api = CTMAPI()
        response = ctm_api.get_calls(account_id, page, request.GET)
        return Response(response)

    def post(self, request, account_id=None, call_id=None):
        data = request.data
        ctm_api = CTMAPI()
        response = ctm_api.update_call(account_id, call_id, data)
        return Response(response)


class CallsSaleUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, account_id=None, call_id=None):
        data = request.data
        ctm_api = CTMAPI()
        response = ctm_api.update_call_sale(account_id, call_id, data)
        return Response(response)


class CallsTagView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, account_id=None):
        ctm_api = CTMAPI()
        response = ctm_api.get_tags(account_id)
        return Response(response)


class CallAudioView(APIView):

    def get(self, request, account_id=None, call_sid=None):
        ctm_api = CTMAPI()
        audio_response = ctm_api.get_call_audio(account_id, call_sid, request)
        size = len(audio_response.content)
        response = HttpResponse(audio_response.content)
        response['Content-Type'] = 'audio/x-wav'
        response['Content-Length'] = size
        response['Accept-Ranges'] = 'bytes'
        response['Content-Range'] = audio_response.headers.get('Content-Range')
        return response
