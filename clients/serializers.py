from rest_framework import serializers
from clients.models import Client


class ClientSerializer(serializers.ModelSerializer):
    total_income = serializers.FloatField(read_only=True)

    class Meta:
        model = Client
        fields = ('id', 'name', 'address', 'email', 'created_at', 'total_income')


