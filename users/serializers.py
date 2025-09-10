from django.contrib.auth.models import User
from rest_framework import serializers
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'roles')
        extra_kwargs = {'password': {'write_only': True}}

    def create (self, validated_data):
        roles = validated_data.pop('roles', [])
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )

        user.roles.set(roles)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'roles')
