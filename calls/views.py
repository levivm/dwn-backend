from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from utils.ctm import CTMAPI

from .dummy_data import DUMMY_RESPONSE


class CallsGetCreateView(APIView):

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

    def post(self, request, account_id=None, call_id=None):
        data = request.data
        ctm_api = CTMAPI()
        response = ctm_api.update_call_sale(account_id, call_id, data)
        return Response(response)


class CallsTagView(APIView):

    def get(self, request, account_id=None):
        ctm_api = CTMAPI()
        response = ctm_api.get_tags(account_id)
        return Response(response)

# class CallsTagView(ListAPIView):
#     serializer_class = TagsSerializer
#     queryset = Tag.objects.all()


class CallAudioView(APIView):

    def get(self, request, account_id=None, call_id=None):
        url = "https://my.callsumo.com/api/v1/accounts/36039/calls/CA6833625884d0e681a1a3a71f6897bff7/recording"
        import base64
        from wsgiref.util import FileWrapper
        from django.http import StreamingHttpResponse
        import pdb
        pdb.set_trace()
        ctm_api = CTMAPI()
        response = ctm_api.get_call_audio(account_id, call_id)
        # short_report = open("somePdfFile", 'rb')
        response = StreamingHttpResponse(FileWrapper(response.raw), content_type='audio/mpeg')
        return response

        # return Response(response)