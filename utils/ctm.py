import json
import base64
import requests

from rest_framework import status
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

    def post(self, endpoint, data=None):
        url = "%s%s%s" % (self.CTM_HOST, self.CTM_API_V, endpoint)
        response = requests.post(url, data=json.dumps(data), headers=self.headers)
        return response

    def put(self, endpoint, data=None):
        url = "%s%s%s" % (self.CTM_HOST, self.CTM_API_V, endpoint)
        response = requests.put(url, data=json.dumps(data), headers=self.headers)
        return response

    def get_calls(self, account_id, page, query_params=None):
        endpoint = '/accounts/%s/calls?%s' % (account_id, query_params.urlencode())
        return self.get(endpoint)

    def get_calls_report(self, account_id, query_params=None):
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
        return self.post(endpoint, data).json()

    def update_call_sale(self, account_id, call_id, data):
        endpoint = '/accounts/%s/calls/%s/sale' % (account_id, call_id)
        return self.post(endpoint, data).json()

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

    def get_numbers(self, account_id, query_params=None):
        endpoint = '/accounts/%s/numbers/search.json?%s' % (
            account_id,
            query_params.urlencode()
        )
        return self.get(endpoint)

    def update_tracking_number_routes(self, account_id, tracking_number_id, data):
        """
            Update tracking number routes
            CTM Endpoint: /accounts/{{account_id}}/numbers/{{number_id}}/dial_routes
            CTM Endpoint METHOD: PUT
        """
        endpoint = '/accounts/%s/numbers/%s/dial_routes' % (
            account_id,
            tracking_number_id
        )
        return self.put(
            endpoint,
            data
        ).json()

    def update_source_tracking_number(self, account_id, tracking_source_id, tracking_number_id):
        endpoint = '/accounts/%s/sources/%s/numbers/%s/add' % (
            account_id,
            tracking_source_id,
            tracking_number_id
        )
        return self.post(endpoint).json()

    def create_receiving_number(self, account_id, receiving_number):
        endpoint = '/accounts/%s/receiving_numbers/' % (account_id)
        data = {
            'number': receiving_number
        }
        return self.post(
            endpoint,
            data
        ).json()

    def update_receiving_number(self, account_id, tracking_number_id, receiving_number_id):
        endpoint = '/accounts/%s/numbers/%s/receiving_numbers/%s/add' % (
            account_id,
            tracking_number_id,
            receiving_number_id
        )
        return self.post(endpoint).json()

    def create_target_number(self, account_id, target_number):
        endpoint = '/accounts/%s/target_numbers/' % (account_id)
        data = {
            'number': target_number
        }
        return self.post(
            endpoint,
            data
        ).json()

    def update_target_number(self, account_id, tracking_number_id, target_number_id):
        endpoint = '/accounts/%s/numbers/%s/target_numbers/%s/add' % (
            account_id,
            tracking_number_id,
            target_number_id
        )
        return self.post(endpoint).json()

    def _create_and_update_target_number(self, account_id, tracking_number_id, target_number):

        response = self.create_target_number(
            account_id,
            target_number
        )

        target_number_id = response.get('call_setting').get('id')

        self.update_target_number(
            account_id,
            tracking_number_id,
            target_number_id
        )

    def _create_and_update_receiving_number(self, account_id,
                                            tracking_number_id, receiving_number):

        response = self.create_receiving_number(
            account_id,
            receiving_number
        )
        receiving_number_id = response.get('receiving_number').get('id')

        self.update_target_number(
            account_id,
            tracking_number_id,
            receiving_number_id
        )

    def update_tracking_number(self, account_id, data):
        """
            May update source, target number or receiving number for a given trancking number
        """
        tracking_number_id = data.get('tracking_number_id')
        tracking_source_id = data.get('tracking_source_id')
        receiving_number_id = data.get('receiving_number_id')
        receiving_number = data.get('receiving_number')
        target_number_id = data.get('target_number_id')
        target_number = data.get('target_number')

        # Update target number for a tracking number
        if receiving_number_id:
            self.update_receiving_number(
                account_id,
                tracking_number_id,
                receiving_number_id
            )

        # Create receiving number for a tracking number
        if not receiving_number_id and receiving_number:
            self._create_and_update_receiving_number(
                account_id,
                tracking_number_id,
                receiving_number
            )

        # Update source for a tracking number
        if tracking_source_id:
            self.update_source_tracking_number(
                account_id,
                tracking_source_id,
                tracking_number_id
            )

        # Update target number for a tracking number
        if target_number_id:
            self.update_target_number(
                account_id,
                tracking_number_id,
                target_number_id
            )

        # Create target number for a tracking number
        if not target_number_id and target_number:
            self._create_and_update_target_number(
                account_id,
                tracking_number_id,
                target_number_id
            )

    def get_receiving_numbers(self, account_id, page=1, query_params=None):
        all_numbers = query_params.get('all', False)
        endpoint = '/accounts/%s/receiving_numbers/?page=%s' % (
            account_id,
            page
        )
        response = self.get(endpoint)

        if not all_numbers:
            return response

        data = response.get('receiving_numbers')
        while not page == response.get('total_pages'):
            next_url = '/accounts/%s/receiving_numbers/?page=%s' % (
                account_id,
                page
            )
            response = self.get(next_url)
            data += response.get('receiving_numbers')
            page += 1

        return {
            'receiving_numbers': data
        }

    def buy_numbers(self, account_id, numbers):
        numbers_response = []
        for number_data in numbers:
            data = {
                'phone_number': number_data.get('phone_number'),
                'test': True
            }
            endpoint = '/accounts/%s/numbers/' % (
                account_id,
            )
            # response = self.post(
            #     endpoint,
            #     data
            # )
            response = {'status': 'success', 'number': {'route_to': {'multi': True, 'type': 'receiving_number', 'mode': 'simultaneous', 'dial': []}, 'formatted': '(253) 299-4672', 'next_billing_date': None, 'active': True, 'status': 'active', 'call_setting': {'id': 'NCF5B75DB2863BDEA0F08BC29BC5FB4A2C01F0309C067498C29159F258C3A8536CF', 'name': 'Account Level', 'url': 'https://api.calltrackingmetrics.com/api/v1/accounts/36039/call_settings/NCF5B75DB2863BDEA0F08BC29BC5FB4A2C01F0309C067498C29159F258C3A8536CF'}, 'purchased_time': '2017-03-14T02:54:25Z', 'stats': {'minute_costs': '0.0', 'since': 1489460065.1714203, 'renewal_costs': '1.5', 'minutes': '0', 'calls': 0}, 'number': '+12532994672', 'routing': 'simultaneous', 'id': 'TPNC3C4B23C348AEC2EE54EFD301979CD2E0CFEF5869D600434C59BFAF7A7617E23', 'country_code': '1', 'name': None, 'account_id': '36039', 'split': ['1', '253', '299', '4672'], 'filter_id': 673531, 'source': None, 'url': 'https://api.calltrackingmetrics.com/api/v1/accounts/36039/numbers/TPNC3C4B23C348AEC2EE54EFD301979CD2E0CFEF5869D600434C59BFAF7A7617E23.json'}}
            if True:
            # if response.status_code == status.HTTP_200_OK:
                # _response = response.json().get('number')
                _response = response.get('number')
                number_response = dict(
                    (
                        k,
                        _response[k]
                    ) for k in (
                        'call_setting',
                        'formatted',
                        'number',
                        'country_code',
                    )
                )
                numbers_response.append(number_response)

        return numbers_response
