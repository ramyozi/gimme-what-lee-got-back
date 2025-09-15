from rest_framework import serializers
from accounts.models import Account

# sérializer pour retourner les infos d'un utilisateur
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'first_name','last_name', 'email', 'role')
