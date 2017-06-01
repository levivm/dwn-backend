from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .callsumo_report import CallSumoReport
from .jotform_report import JotFormReport
from .serializers import JotFormRequestReportSerializer, JotFormAppointmentRequestsSerializer


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
        # Get request data
        data = request.data

        # Set serializer to validate request data
        serializer = JotFormRequestReportSerializer(data=data)

        # Check if data given to serializer is valid
        serializer.is_valid(raise_exception=True)

        # Init jotform report instance
        jotform_report = JotFormReport()

        # Get submission reports
        submissions = jotform_report.submissions_report(
            serializer.data.get('start_date'),
            serializer.data.get('end_date'),
        )

        # Insert submissions data into serialiazer for parsing
        response_serializer = JotFormAppointmentRequestsSerializer(
            data=submissions,
            many=True
        )

        # Check if fetched data is valid
        response_serializer.is_valid()

        # Get response data from valid serializer
        response = response_serializer.data

        return Response(response)
