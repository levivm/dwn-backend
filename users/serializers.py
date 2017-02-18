from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from accounts.serializers import MembershipSerializer

from .models import Profile
from .roles import *


class UsersSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )

    @classmethod
    def check_email(cls, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email already used")
        return email

    def validate(self, data):
        first_name = data['first_name']
        last_name = data['last_name']
        username = Profile.generate_username(first_name, last_name)
        data['username'] = username
        return data

    def create(self, validated_data):

        # Validate email
        UsersSerializer.check_email(validated_data['email'])

        request = self.context.get('request')
        password = request.data.get('user').get('password')
        user = super(UsersSerializer, self).create(validated_data)

        # Set user password
        user.set_password(password)
        user.save()
        return user


class ProfilesSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    current_account_role = serializers.SerializerMethodField()
    accounts_roles = serializers.SerializerMethodField()
    available_accounts = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'id',
            'user',
            'telephone',
            'current_account_role',
            'accounts_roles',
            'agency_admin',
            'available_accounts'
        )

    def get_available_accounts(self, obj):
        return MembershipSerializer(instance=obj.membership_set.all(), many=True).data\
            if obj.agency_admin \
            else MembershipSerializer(obj.membership_set.filter(role=ADMIN_ROLE), many=True).data

    def get_accounts_roles(self, obj):
        roles = ROLES_CHOICES
        roles_data = [{'role': {'name': role, 'name_display': role_display}, 'accounts':
                      MembershipSerializer(instance=obj.membership_set.filter(role=role),
                                           remove_fields=['profile', 'role'],
                                           many=True).data}
                      for role, role_display in roles]
        return roles_data

    def get_current_account_role(self, obj):
        request = self.context.get('request')
        if not request:
            return
        account_id = request.parser_context\
            .get('kwargs', {}).get('account_id')
        if not account_id:
            return

        membership = obj.membership_set.filter(account__call_metrics_id=account_id).first()
        return membership.get_role_display() if membership else None

    def assign_role(self, data, profile):
        memberhsip_data = {
            'role': data.get('role'),
            'account': data.get('account'),
            'profile': profile.id
        }
        serializer = MembershipSerializer(data=memberhsip_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def assign_roles(self, accounts_roles=None, profile=None):
        profile.membership_set.all().delete()
        for value in accounts_roles:
            role = value.get('role').get('name')
            accounts = value.get('accounts')
            for account_data in accounts:
                data = {
                    'account': account_data.get('account'),
                    'role': role,
                    'profile': profile.id
                }
                serializer = MembershipSerializer(data=data)

                serializer.is_valid(raise_exception=True)
                serializer.save()

    def create(self, validated_data):

        # Create user
        user_data = validated_data.pop('user')
        serializer = UsersSerializer(data=user_data,
                                     context={'request': self.context.get('request')})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        profile = Profile.objects.create(user=user, **validated_data)

        # create user token
        Token.objects.get_or_create(user=user)

        # Create roles
        data = self.context.get('request').data
        if not data.get('role') or not data.get('account'):
            raise serializers.ValidationError({'role': ["Must select a role"]})
        self.assign_role(data, profile)

        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        instance.update_user(user_data)

        # Validate email
        email = user_data.get('email')
        if not self.instance.user.email == email:
            UsersSerializer.check_email(email)

        # Create roles
        data = self.context.get('request').data
        self.assign_roles(**{'accounts_roles': data.get('accounts_roles'),
                          'profile': instance})

        return super(ProfilesSerializer, self).update(instance, validated_data)
