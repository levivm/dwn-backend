from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response


from users.serializers import ProfilesSerializer
from users.models import Profile
from users.roles import ROLES_ACCESS_LEVEL


from .serializers import AuthTokenSerializer


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
