import operator
import json

from utils.jotform import JotFormAPI
from utils.filters_mixin import FilterMixin

from .mixins import ReportByEmailMixin


class JotFormReport(FilterMixin, ReportByEmailMixin):
    """
        A report getting data from JotForm using their API
    """
    APPOINTMENT_FORM_STR = 'Appointment Form'

    def __init__(self, office_name=None, *args, **kwargs):
        """
         Attributes:
            jotform_api Instance for getting access to JotForm API
            office_name The office name used to fetch data from JotForm
        """
        self.jotform_api = JotFormAPI()
        self.office_name = office_name

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

        return filtered_forms.pop() if filtered_forms else []

    def submissions_report(self, type, start_date, end_date):
        # start_date = params.get('start_date')
        # end_date = params.get('end_date')
        filters = {
            "created_at:gt": start_date,
            "created_at:lt": end_date,
        }

        # Get appointment form for given office name
        form = self.get_form_by_keywords(
            *[
                self.office_name,
                type
            ]
        )

        if not form:
            return []

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

        submissions = self._parse_submission(submissions.get('content'))

        return submissions

    @staticmethod
    def _get_answer(value, answers):
        if not answers:
            return {}
        answer = list(filter(
            lambda answer: value in answer[1].get('text').lower(),
            answers.items()
        ))
        return answer.pop()[1] if answer else {}

    @classmethod
    def _parse_submission(cls, submissions):
        parsed_submissions = []

        # Mapping between serializer submission desired fields and fields present
        # on submission data response from JOTFORM API
        attribute_match = {
            'name': 'name',
            'phone': 'phone',
            'email': 'e-mail',
            'detail': 'are you'
        }

        # Get form details from each submission
        for submission in submissions:
            # Get answer from submission data
            answers = submission.get('answers')

            # Get answer from submission data for each attribute defined
            # in `attribute_match` dictionary
            # we fetch answer from `prettyFormat` attribute or `answer`
            parsed_submission = {
                key: cls._get_answer(
                    value,
                    answers
                ).get(
                    'prettyFormat',
                    cls._get_answer(
                        value,
                        answers
                    ).get('answer')
                )
                for key, value in attribute_match.items()
            }

            # Add date submitted attribute to parse submission data
            parsed_submission.update({
                'date_submitted': submission.get('created_at')
            })

            # Append parsed submission data to all parsed submissions
            parsed_submissions.append(parsed_submission)

        return parsed_submissions
