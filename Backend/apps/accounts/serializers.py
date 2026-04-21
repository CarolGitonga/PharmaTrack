from rest_framework import serializers
from .models import CustomUser, Pharmacy


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = ['id', 'name', 'owner_name', 'phone', 'email', 'location', 'plan']


class UserSerializer(serializers.ModelSerializer):
    pharmacy = PharmacySerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'pharmacy']
