from datetime import datetime, timedelta
from rest_framework import serializers


class PatientsReportSerializer(serializers.Serializer):
    source = serializers.CharField()
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    email = serializers.CharField()
    homephone = serializers.CharField()
    workphone = serializers.CharField()
    cell = serializers.CharField()


class JotFormRequestReportSerializer(serializers.Serializer):
    TYPES_CHOICES = (
        ('Appointment', 'appointment'),
        ('Contact', 'contact')
    )
    start_date = serializers.CharField()
    end_date = serializers.CharField()
    type = serializers.ChoiceField(TYPES_CHOICES)
    office_name = serializers.CharField()

    def validate_start_date(self, date_str):
        try:
            _date = datetime.strptime(date_str, "%Y-%m-%d")
            date = _date - timedelta(days=1)
        except ValueError:
            raise serializers.ValidationError("Date format is wrong")
        return datetime.strftime(date, "%Y-%m-%d")

    def validate_end_date(self, date_str):
        try:
            _date = datetime.strptime(date_str, "%Y-%m-%d")
            date = _date + timedelta(days=1)
        except ValueError:
            raise serializers.ValidationError("Date format is wrong")
        return datetime.strftime(date, "%Y-%m-%d")


class JotFormAppointmentRequestsSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    detail = serializers.CharField(required=False)
    date_submitted = serializers.CharField(required=False)
