
import itertools
from collections import OrderedDict

from .serializers import PatientsReportSerializer

from utils.ctm import CTMAPI
from utils.legacy_db import CallSumoLegacyDB


class CallSumoReport:

    def __init__(self, account_id=None, *args, **kwargs):
        self.ctm_api = CTMAPI()
        self.account_id = account_id

    def _get_sources(self):
        """
            Method to get all sources for an account from CTM API
        """
        # Get source data from CTM API
        _source_data = self.ctm_api.get_sources(self.account_id)
        source_data = _source_data.get('sources')

        # Map filter_id and name attributes from source_data
        sources = [
            {
                'filter_id': source.get('filter_id'),
                'name': source.get('name')
            } for source in source_data
        ]

        return sources

    def _get_new_patients_numbers_from_sikka(self, start_date, end_date):
        # Create db instance
        callsumo_db = CallSumoLegacyDB()

        # Get new patients
        new_patients = callsumo_db.get_new_patients_by_created_date(
            start_date,
            end_date,
            self.account_id
        )

        phones_numbers = []

        if not new_patients:
            return [
                phones_numbers,
                new_patients
            ]

        # Create a list containing all numbers from new detected patients
        for patient in new_patients:
            phones_numbers = list(
                itertools.chain(
                    phones_numbers,
                    [patient.get(
                        'workphone',
                        []
                    )],
                    [patient.get(
                        'cell',
                        []
                    )],
                    [patient.get(
                        'homephone',
                        []
                    )],
                )
            )

        return [phones_numbers, new_patients]

    @staticmethod
    def _remove_number_format(number):
        return number.replace(
            '(',
            ''
        ).replace(
            ')',
            ''
        ).replace(
            '-',
            ''
        ).replace(
            ' ',
            ''
        )

    @staticmethod
    def _parse_new_patients_by_source_response(
        new_patients,
        new_patients_by_source
    ):

        new_patients_data = PatientsReportSerializer(
            new_patients,
            many=True
        ).data

        # Order new_patients using fields_to_display list order
        new_patients_by_source_data = OrderedDict(
            sorted(
                new_patients_by_source.items(),
                key=lambda s: s
            )
        )

        return [
            new_patients_data,
            new_patients_by_source_data
        ]

    def get_new_patients_by_source(self, start_date, end_date):

        new_patients_by_source = {}
        new_patients_from_callsumo = []

        # start_date = '2016-10-01'
        # end_date = '2016-10-31'

        # Get account available sources
        sources = self._get_sources()

        # Init calls by source amount dict, assigning 0 to all sources
        new_patients_by_source = {source.get('name'): 0 for source in sources}

        # Set filters by date
        filters = {
            'start_date': start_date,
            'end_date': end_date,
        }

        # Get all calls from account_id parameters and filter by range date
        calls_data = self.ctm_api.get_calls_all(self.account_id, filters)

        # Create a dictionary for calls data using caller_number_bare as key
        calls = {call.get('caller_number_bare'): call for call in calls_data}

        # Get a list with all new phones numbers and all new patients for self.account_id
        # given a date range
        new_phones_numbers, new_patients = self._get_new_patients_numbers_from_sikka(
            start_date,
            end_date
        )

        if not new_patients:
            return [
                [],
                new_patients_by_source
            ]

        for patient in new_patients:
            # Get workphone, cell and homephone numbers from a patient
            patient_phone_numbers = [
                patient.get(
                    'workphone',
                    None
                ),
                patient.get(
                    'cell',
                    None
                ),
                patient.get(
                    'homephone',
                    None
                )
            ]

            # Remove format number (xxx) xxx-xxxxx -> xxxxxxxxxxx
            patient_phone_numbers = list(map(
                self._remove_number_format,
                patient_phone_numbers
            ))

            # Check if any patient's number exists on callsumo calls log.
            if any(self._remove_number_format(number) in calls
                   for number in patient_phone_numbers):

                # Dump patient workphone, cell and homephone numbers into vars
                workphone, cell, homephone = patient_phone_numbers

                # For any existing patient's number get it's source from callsumo call data
                call_source = calls.get(
                    workphone,
                    calls.get(
                        homephone,
                        calls.get(
                            cell,
                        )
                    )
                ).get('source')

                # Append source to patient data
                patient.update({
                    'source': call_source
                })

                # Update calls by source counter
                new_patients_by_source.update({
                    call_source: new_patients_by_source.get(call_source) + 1
                })

                # Append this patient to new patients from callsumo
                new_patients_from_callsumo.append(patient)

        return self._parse_new_patients_by_source_response(
            new_patients_from_callsumo,
            new_patients_by_source
        )
