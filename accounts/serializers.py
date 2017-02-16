from rest_framework import serializers

from utils.serializers import RemovableFieldsMixin

from .models import Account, Membership


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'call_metrics_id',
            'name'
        )


class MembershipSerializer(RemovableFieldsMixin, serializers.ModelSerializer):
    account = serializers.\
        SlugRelatedField(queryset=Account.objects.all(),
                         slug_field='call_metrics_id')

    class Meta:
        model = Membership
        fields = (
            'account',
            'profile',
            'role',
            'account_name',
        )
