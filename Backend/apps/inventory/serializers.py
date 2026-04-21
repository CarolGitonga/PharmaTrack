from rest_framework import serializers
from .models import Medicine, StockMovement


class MedicineSerializer(serializers.ModelSerializer):
    is_low_stock = serializers.ReadOnlyField()
    is_expiring_soon = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    days_to_expiry = serializers.ReadOnlyField()

    class Meta:
        model = Medicine
        fields = [
            'id', 'name', 'generic_name', 'category', 'manufacturer',
            'batch_number', 'quantity', 'minimum_quantity', 'buying_price',
            'selling_price', 'expiry_date', 'supplier', 'unit', 'is_active',
            'created_at', 'updated_at',
            'is_low_stock', 'is_expiring_soon', 'is_expired', 'days_to_expiry',
        ]
        read_only_fields = ['created_at', 'updated_at']


class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ['id', 'medicine', 'movement_type', 'quantity', 'notes', 'performed_by', 'date']
        read_only_fields = ['date']
