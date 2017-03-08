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

    def get(self, endpoint):
        url = "%s%s%s" % (self.CTM_HOST, self.CTM_API_V, endpoint)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_file(self, endpoint, content_type, range_header=None):
        url = "%s%s%s" % (self.CTM_HOST, self.CTM_API_V, endpoint)
        self.headers.update({
            'Content-Type': content_type
        })
        if range_header:
            self.headers.update({
                'Range': range_header
            })
        response = requests.get(url, headers=self.headers)
        return response

    def post(self, endpoint, data):
        url = "%s%s%s" % (self.CTM_HOST, self.CTM_API_V, endpoint)
        response = requests.post(url, data=json.dumps(data), headers=self.headers)
        return response.json()

    def get_calls(self, account_id, page, query_params=None):
        endpoint = '/accounts/%s/calls?%s' % (account_id, query_params.urlencode())
        return self.get(endpoint)

    def get_calls_report(self, account_id, query_params=None):
        #start_date=2017-02-01&end_date=2017-02-28&with_time=1&by=source
        endpoint = "/accounts/%s/reports/series?%s" % (account_id, query_params.urlencode())
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

    def get_call_audio(self, account_id, call_sid, request):
        endpoint = '/accounts/%s/calls/%s/recording' % (account_id, call_sid)
        content_type = 'audio/wav'
        range_header = request.META.get("HTTP_RANGE")
        return self.get_file(endpoint, content_type, range_header)

    def get_all_accounts(self):
        endpoint = '/accounts?names=1&all=1'
        return self.get(endpoint)

    def get_users_account(self, account_id):
        endpoint = '/accounts/%s/users/' % (account_id,)
        return self.get(endpoint)

    def get_all_users(self, account_id, page=1):
        endpoint = '/accounts/%s/users/?page=%s' % (
            account_id,
            page
        )
        response = self.get(endpoint)
        data = response.get('users')
        while response.get('next_page'):
            next_url = '/accounts/%s/users/?page=%s' % (
                account_id,
                page
            )
            response = self.get(next_url)
            data += response.get('users')
            page += 1

        return data



# data-audio-mp3="https://my.callsumo.com/api/v1/accounts/36039/calls/CA6833625884d0e681a1a3a71f6897bff7/recording.mp3"