from rest_framework import serializers
from .models import CustomUser, RoleChoices

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        request = self.context.get('request')
        role = validated_data.get('role', RoleChoices.USER)

        # Vérification sécurité pour création d'admin
        if role == RoleChoices.ADMIN:
            if not request or not request.user.is_authenticated or not request.user.is_admin():
                raise serializers.ValidationError("Need admin privileges to create an admin user.")

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=role
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role')
