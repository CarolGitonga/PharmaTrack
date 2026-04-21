from django.contrib import admin
from .models import Medicine, StockMovement


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'pharmacy', 'category', 'quantity', 'minimum_quantity', 'expiry_date', 'is_active')
    list_filter = ('category', 'pharmacy', 'is_active')
    search_fields = ('name', 'generic_name', 'batch_number')


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'movement_type', 'quantity', 'performed_by', 'date')
    list_filter = ('movement_type', 'pharmacy')
