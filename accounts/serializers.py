from rest_framework import serializers
from .models import Account, RoleChoices

# sérializer pour l'inscription
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    # création sécurisée d'un utilisateur avec contrôle pour admin
    def create(self, validated_data):
        request = self.context.get('request')
        role = validated_data.get('role', RoleChoices.MEMBER)

        # Vérification sécurité pour création d'admin
        if role == RoleChoices.ADMIN:
            if not request or not request.user.is_authenticated or not request.user.is_admin():
                raise serializers.ValidationError("Need admin privileges to create an admin user.")

        user = Account.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=role
        )
        return user

# sérializer pour retourner les infos d'un utilisateur
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'role')
