from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .callsumo_report import CallSumoReport
from .jotform_report import JotFormReport


class NewPatientsReportView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, account_id=None):
        data = request.data
        callsumo_report = CallSumoReport(
            account_id=data.get('ctm_account_id')
        )
        response = callsumo_report.get_new_patients_by_source(
            data.get('start_date'),
            data.get('end_date')
        )

        return Response(response)


class JotFormSubmissionsReportView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, account_id=None):
        data = request.data
        jotform_report = JotFormReport()
        response = jotform_report.submissions_report(data)
        import pprint
        pprint.pprint(response)
        return Response(response)
