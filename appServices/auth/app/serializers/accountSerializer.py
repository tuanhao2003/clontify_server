from rest_framework import serializers
from app.entities.accounts import Accounts

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        exclude = ['password']