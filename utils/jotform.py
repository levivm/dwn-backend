import requests
from urllib.parse import urlencode

from django.conf import settings


class JotFormAPI:

    JOTFORM_API_KEY = settings.JOTFORM_API_KEY
    JOTFORM_HOST = settings.JOTFORM_HOST

    def __init__(self):
        self.headers = {
            'APIKEY': '%s' % (self.JOTFORM_API_KEY),
            'Content-Type': 'application/json'
        }

    def get(self, endpoint):
        url = "%s%s" % (
            self.JOTFORM_HOST,
            endpoint
        )
        response = requests.get(
            url,
            headers=self.headers
        )
        return response

    def get_forms(self):
        """
            Get all JOTFORM forms for our company user
            JOTFORM Endpoint: /users/forms
            JOTFORM Method: GET
        """
        endpoint = '/user/forms'
        return self.get(endpoint).json()

    def get_form_submissions(self, form_id=None, query_params=None):
        """
            Get all form submissions given a date range
            JOTFORM Endpoint: /form/{id}/submissions
            JOTFORM Method: GET
        """

        # Encode GET query_params object or a normal dict
        query_params = urlencode(query_params) \
            if (isinstance(
                query_params,
                dict
            )) else query_params.urlencode()

        # Endpoint for fetch all form's submissions
        endpoint = '/form/%s/submissions?%s' % (
            form_id,
            query_params
        )

        return self.get(endpoint).json()
