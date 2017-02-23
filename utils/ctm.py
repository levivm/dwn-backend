import json
import base64
import requests

from django.conf import settings
from django.http import QueryDict


class CTMAPI():

    CTM_TOKEN = settings.CTM_TOKEN
    CTM_SECRET = settings.CTM_SECRET
    CTM_HOST = settings.CTM_HOST
    CTM_API_V = settings.CTM_API_V
    CALLSUMO_HOST = settings.CALLSUMO_HOST

    def __init__(self):
        code = ('%s:%s' % (self.CTM_TOKEN, self.CTM_SECRET)).encode('ascii')
        self.auth = base64.standard_b64encode(bytes(code)).decode()
        self.headers = {
            'authorization': 'Basic %s' % self.auth,
            'Content-Type': 'application/json'
        }
        print(self.auth)

    def get(self, endpoint):
        url = "%s%s%s" % (self.CTM_HOST, self.CTM_API_V, endpoint)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_file(self, endpoint, content_type):
        url = "%s%s%s" % (self.CALLSUMO_HOST, self.CTM_API_V, endpoint)
        # self.headers.update({
            # 'Content-Type': content_type
        # })
        print(url)

        response = requests.get(url, headers=self.headers)
        return response

    def post(self, endpoint, data):
        url = "%s%s%s" % (self.CTM_HOST, self.CTM_API_V, endpoint)
        response = requests.post(url, data=json.dumps(data), headers=self.headers)
        return response.json()

    def get_calls(self, account_id, page, query_params=None):
        endpoint = '/accounts/%s/calls?%s' % (account_id, query_params.urlencode())
        return self.get(endpoint)

    def get_tags(self, account_id):
        endpoint = '/accounts/%s/tags/' % (account_id,)
        return self.get(endpoint)

    def get_sources(self, account_id):
        endpoint = '/accounts/%s/sources/' % (account_id,)
        return self.get(endpoint)

    def update_call(self, account_id, call_id, data):
        endpoint = '/accounts/%s/calls/%s/modify' % (account_id, call_id)
        return self.post(endpoint, data)

    def update_call_sale(self, account_id, call_id, data):
        endpoint = '/accounts/%s/calls/%s/sale' % (account_id, call_id)
        return self.post(endpoint, data)

    def get_call_audio(self, account_id, call_id):
        # response = self.get(url)
        endpoint = '/accounts/%s/calls/%s/recording.mp3' % (36039, 'CA6833625884d0e681a1a3a71f6897bff7')
        content_type = 'audio/mpeg'
        return self.get_file(endpoint, content_type)

# data-audio-mp3="https://my.callsumo.com/api/v1/accounts/36039/calls/CA6833625884d0e681a1a3a71f6897bff7/recording.mp3"