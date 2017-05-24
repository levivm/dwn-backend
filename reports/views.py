from rest_framework.views import APIView
from rest_framework.response import Response

from .callsumo_report import CallSumoReport


class NewPatientsReportView(APIView):
#    permission_classes = (IsAuthenticated,)

    def get(self, request, account_id=None):
        # ctm_api = CTMAPI()
        data = request.data
        print(data)
        callsumo_report = CallSumoReport(
            account_id=data.get('ctm_account_id')
        )
        response = callsumo_report.get_new_patients_by_source(
            data.get('start_date'),
            data.get('end_date')
        )

        return Response(response)
