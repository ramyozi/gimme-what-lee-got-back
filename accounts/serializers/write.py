from rest_framework import serializers
from accounts.models import Account, RoleChoices

# sérializer pour l'inscription
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'email','first_name','last_name', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        request = self.context.get('request')
        role = validated_data.get('role', RoleChoices.MEMBER)

        # sécurité pour création d'un admin
        if role == RoleChoices.ADMIN:
            if not request or not request.user.is_authenticated or not request.user.is_admin():
                raise serializers.ValidationError("Need admin privileges to create an admin user.")

        user = Account.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=role
        )
        return user
