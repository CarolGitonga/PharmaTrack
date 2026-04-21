from django.db import models
from apps.accounts.models import Pharmacy
from apps.inventory.models import Medicine


class AlertLog(models.Model):
    ALERT_TYPES = [
        ('LOW_STOCK', 'Low Stock'),
        ('EXPIRING_60', 'Expiring in 60 days'),
        ('EXPIRING_30', 'Expiring in 30 days'),
        ('EXPIRED', 'Expired'),
    ]
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    message = models.TextField()
    sent_to = models.CharField(max_length=20)
    sent_at = models.DateTimeField(auto_now_add=True)
    was_successful = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.alert_type} — {self.medicine.name} ({self.sent_at.date()})"
