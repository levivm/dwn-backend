from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from rest_framework import serializers, exceptions
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        data['user'] = user
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise exceptions.ValidationError('User does not exist')


class ResetPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 != password2:
            raise serializers.ValidationError("The new password doesn't match.")

        uidb64 = data.get('uidb64')
        token = data.get('token')
        uid = int(urlsafe_base64_decode(uidb64))
        try:
            user = User.objects.get(pk=uid)
            if not default_token_generator.check_token(user, token):
                raise serializers.ValidationError("The reset password link is no longer valid.")
        except User.DoesNotExist:
            raise serializers.ValidationError("The reset password link is no longer valid.")

        return data


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate_password(self, password):
        user = self.context['user']
        if not user.check_password(password):
            raise serializers.ValidationError(_('The current password is incorrect.'))
        return password

    def validate(self, data):
        password1 = data['password1']
        password2 = data['password2']

        if password1 != password2:
            raise serializers.ValidationError(_("The new password doesn't match."))

        return data
