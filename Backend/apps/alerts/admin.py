from django.contrib import admin
from .models import AlertLog


@admin.register(AlertLog)
class AlertLogAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'alert_type', 'sent_to', 'sent_at', 'was_successful')
    list_filter = ('alert_type', 'was_successful', 'pharmacy')
