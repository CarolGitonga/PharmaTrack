from rest_framework import serializers
from .models import AlertLog


class AlertLogSerializer(serializers.ModelSerializer):
    medicine_name = serializers.SerializerMethodField()

    def get_medicine_name(self, obj):
        return obj.medicine.name if obj.medicine else 'Test SMS'

    class Meta:
        model = AlertLog
        fields = ['id', 'medicine', 'medicine_name', 'alert_type', 'message', 'sent_to', 'sent_at', 'was_successful']
