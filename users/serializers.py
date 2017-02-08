from rest_framework import serializers, exceptions
from django.contrib.auth.models import User
from .models import Profile


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class ProfilesSerializer(serializers.ModelSerializer):
    user = UsersSerializer()

    class Meta:
        model = Profile
        fields = (
            'user',
            'telephone',
        )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        profile = Profile.objects.create(user=user, **validated_data)
        return profile
