import json
import copy
import base64
import requests
from urllib.parse import urlencode
from collections import OrderedDict


from django.conf import settings

from utils.filters_mixin import FilterMixin
from utils.legacy_db import CallSumoLegacyDB


class CTMAPI(FilterMixin):

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

        # # If not untagged_calls flag is present, return normal  calls
        if not query_params.get('untagged_calls'):
            return self.get(endpoint)

        # Return filtered unique untagged calls from ctm calls response
        return self.get_untagged_calls(
            account_id,
            page,
            query_params
        )

    def get_untagged_calls(self, account_id, page, query_params=None):
        # Get calls response
        endpoint = '/accounts/%s/calls?%s' % (
            account_id,
            query_params.urlencode()
        )
        calls_response_ = self.get(endpoint)

        calls_response = copy.deepcopy(calls_response_)

        calls = calls_response.get(
            'calls',
            []
        )

        # Created ordered dict for grouping calls
        grouped_calls = OrderedDict()

        # Empty calls
        calls_response.update({
            'calls': []
        })

        # group calls by number
        for call in calls:
            number = call.get('caller_number')
            grouped_calls.update({
                number: grouped_calls.get(
                    number,
                    []
                ) + [call]
            })

        # Init call sumo legacy db
        callsumo_db = CallSumoLegacyDB()

        # Get all phone number from an account
        phone_list = callsumo_db.get_numbers_from_practice(account_id)

        existing_numbers = {}

        # Create a dictionary with fetched number using number as key
        for phone in phone_list:
            existing_numbers.update({
                phone.get('phone_number'): phone
            })

        # Init filtered calls
        filtered_calls = []

        for number, calls in grouped_calls.items():
            # Check if the number is a lead or not
            # depending if it is already an existing number
            # and if no exists check if it only has ar2:autoreported
            # and ar2:lead tags only
            # If the number exists, we mark as lead if it is tagged still
            # as an inquiry
            number_is_lead = all(
                map(
                    lambda call:
                        existing_numbers.get(
                            call.get(
                                'caller_number_bare',
                                '',
                            ),
                            None
                        ) is None and
                        set(call.get(
                            'tag_list',
                            [],
                        )).issubset({
                            'ar2:lead',
                            'ar2:autoreported'
                        }) or (
                            existing_numbers.get(
                                call.get(
                                    'caller_number_bare',
                                    '',
                                ),
                                None
                            ) and 'inquiry' in existing_numbers.get(
                                call.get(
                                    'caller_number_bare',
                                    '',
                                ),
                                {}
                            ).get(
                                'record_type',
                                ''
                            )
                        ),
                    calls
                )
            )

            # If the number is a lead, we add unprocessed tag
            # to it's calls
            if number_is_lead:
                for call in calls:
                    call.update({
                        'unprocessed': True
                    })

            filtered_calls += calls

        # Update calls response with filtered calls
        calls_response.update({
            'calls': filtered_calls
        })

        return calls_response

    def get_unique_untagged_calls(self, account_id, page, query_params=None):

        # Get unique calls response
        unique_calls_response = self.get_unique_calls(
            account_id,
            page,
            query_params
        )

        # Get calls from unique calls response
        calls = unique_calls_response.get(
            'calls',
            []
        )

        # Copy unique calls response to unique calls dict
        unique_untagged_calls = copy.deepcopy(unique_calls_response)

        # Empty calls gotten from unique calls response
        unique_untagged_calls['calls'] = []

        # Get all untagged calls by checking if they have only ar2:lead and
        # ar2:autoreporting tags
        for call in calls:
            tags = call.get('tag_list', [])
            if set(tags).issubset({'ar2:lead', 'ar2:autoreported'}):
                unique_untagged_calls['calls'].append(call)

        return unique_untagged_calls

    def get_calls_all(self, account_id, query_params, page=1):

        query_params = urlencode(query_params) \
            if (isinstance(
                query_params,
                dict
            )) else query_params.urlencode()

        # Get the first page
        endpoint = '/accounts/%s/calls/?page=%s&%s' % (
            account_id,
            page,
            query_params
        )
        response = self.get(endpoint)
        page += 1
        data = response.get('calls')

        # Iterate to get all next pages
        while response.get('next_page'):
            next_url = '/accounts/%s/calls/?page=%s&%s' % (
                account_id,
                page,
                query_params
            )
            response = self.get(next_url)
            data += response.get('calls', [])
            page += 1

        return data

    def get_calls_report(self, account_id, query_params=None):
        endpoint = "/accounts/%s/reports/series?%s" % (account_id, query_params.urlencode())
        return self.get(endpoint)

    def get_tags(self, account_id):
        endpoint = '/accounts/%s/tags/' % (account_id,)
        return self.get(endpoint)

    def get_sources(self, account_id, page=1):
        # Get the first page
        endpoint = '/accounts/%s/sources/?page=%s' % (
            account_id,
            page
        )
        response = self.get(endpoint)
        total_pages = response.get('total_pages', [])
        page += 1
        data = response.get('sources')

        # Iterate to get all next pages
        while page <= total_pages:
            next_url = '/accounts/%s/sources/?page=%s' % (
                account_id,
                page
            )
            response = self.get(next_url)
            data += response.get('sources', [])
            total_pages = response.get('total_pages', [])
            page += 1

        return {'sources': data}

    # def get_sources(self, account_id):
    #     endpoint = '/accounts/%s/sources/' % (account_id,)
    #     return self.get(endpoint)

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

    def get_account_info(self, account_id):
        endpoint = '/accounts/%s' % (account_id,)
        return self.get(endpoint)

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
