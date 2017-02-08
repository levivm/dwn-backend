from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


from users.serializers import ProfilesSerializer
from users.models import Profile

from .serializers import AuthTokenSerializer

# Create your views here.


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
        data = {'token': user.auth_token.key, 'user': profile_data}
        return Response(data)
