from rest_framework import serializers

from .models import Account


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'call_metrics_id',
            'name'
        )
