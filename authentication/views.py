from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


from authentication.serializers import ForgotPasswordSerializer, ResetPasswordSerializer

from utils.mailer import BaseEmail
from users.serializers import ProfilesSerializer
from users.models import Profile, User
from users.roles import ROLES_ACCESS_LEVEL


from .serializers import AuthTokenSerializer
from .mixins import PasswordResetLinkMixin


class LoginView(GenericAPIView):
    """
    Class to login users
    """
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        profile = Profile.objects.get(user=user)
        profile_data = ProfilesSerializer(profile).data
        data = {'token': user.auth_token.key, 'user': profile_data,
                'roles_access_level': ROLES_ACCESS_LEVEL}
        return Response(data)


class ForgotPasswordView(PasswordResetLinkMixin, GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_user()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        context = {
            'user': user,
            'token': token,
            'uid': uid,
            'reset_link': ForgotPasswordView.generate_reset_link(uid, token),
        }
        email_data = {
            'subject': 'Password Reset',
            'to': user.email,
            'context': context,
            'template_name': 'password_reset_email',
            'template_path': 'authentication/emails/'
        }
        email = BaseEmail(**email_data)
        email.send()

        return Response('OK')

    def get_user(self):
        user = User.objects.get(email=self.request.data.get('email'))
        return user


class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, uidb64=None, token=None):
        serializer_data = self.request.data
        serializer_data.update({
            'uidb64': uidb64,
            'token': token
        })
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
        password = serializer.data.get('password1')
        user.set_password(password)
        user.save()
        return Response('OK')
