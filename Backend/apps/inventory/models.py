from django.db import models
from django.utils import timezone
from apps.accounts.models import Pharmacy, CustomUser


class Medicine(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='medicines')
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=200, blank=True)
    batch_number = models.CharField(max_length=100, blank=True)
    quantity = models.IntegerField(default=0)
    minimum_quantity = models.IntegerField(default=10)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()
    supplier = models.CharField(max_length=200, blank=True)
    unit = models.CharField(max_length=50, default='pcs')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.pharmacy})"

    @property
    def is_low_stock(self):
        return self.quantity <= self.minimum_quantity

    @property
    def days_to_expiry(self):
        delta = self.expiry_date - timezone.now().date()
        return delta.days

    @property
    def is_expiring_soon(self):
        return 0 < self.days_to_expiry <= 60

    @property
    def is_expired(self):
        return self.days_to_expiry <= 0


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('ADJUSTMENT', 'Adjustment'),
        ('EXPIRED', 'Expired Removal'),
    ]
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=15, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    notes = models.TextField(blank=True)
    performed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} — {self.medicine.name} x{self.quantity}"
