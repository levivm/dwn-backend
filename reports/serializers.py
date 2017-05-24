from rest_framework import serializers


class PatientsReportSerializer(serializers.Serializer):
    source = serializers.CharField()
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    email = serializers.CharField()
    homephone = serializers.CharField()
    workphone = serializers.CharField()
    cell = serializers.CharField()
