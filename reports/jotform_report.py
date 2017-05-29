import operator
import json

from utils.jotform import JotFormAPI
from utils.filters_mixin import FilterMixin


class JotFormReport(FilterMixin):

    APPOINTMENT_FORM_STR = 'Appointment Form'

    def __init__(self, *args, **kwargs):
        self.jotform_api = JotFormAPI()

    def get_form_by_keywords(self, *keywords):
        forms = self.jotform_api.get_forms().get('content')
        filtered_forms = forms
        for keyword in keywords:
            filtered_forms = self.filter_dicts_by_attribute(
                dicts=filtered_forms,
                attribute='title',
                operator=operator.contains,
                value=keyword
            )

        import pprint
        pprint.pprint(filtered_forms)
        return filtered_forms.pop()

    def submissions_report(self, params):
        start_date = params.get('start_date')
        end_date = params.get('end_date')

        filters = {
            "created_at:gt": self._parse_gt_date_filter(start_date),
            "created_at:lt": self._parse_gt_date_filter(end_date),
        }

        # Get appointment form for given office name
        form = self.get_form_by_keywords(
            *[
                params.get('office_name'),
                params.get('type')
            ]
        )

        # Get form id
        form_id = form.get('id')

        # Built query_params to filter office appointment form filled
        query_params = {
            'filter': json.dumps(filters),
            'limit': 1000
        }

        # Fetch form's submissions given some filters
        submissions = self.jotform_api.get_form_submissions(
            form_id=form_id,
            query_params=query_params
        )

        return submissions

    @staticmethod
    def _parse_gt_date_filter(date):
        return date
