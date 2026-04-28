from rest_framework import serializers
from .models import AlertLog


class AlertLogSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)

    class Meta:
        model = AlertLog
        fields = ['id', 'medicine', 'medicine_name', 'alert_type', 'message', 'sent_to', 'sent_at', 'was_successful']
