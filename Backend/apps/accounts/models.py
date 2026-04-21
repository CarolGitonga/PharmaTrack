from django.contrib.auth.models import AbstractUser
from django.db import models


class Pharmacy(models.Model):
    PLAN_CHOICES = [
        ('starter', 'Starter'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    location = models.CharField(max_length=200)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='starter')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Pharmacies'

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('pharmacist', 'Pharmacist'),
        ('cashier', 'Cashier'),
    ]
    pharmacy = models.ForeignKey(
        Pharmacy, on_delete=models.CASCADE,
        null=True, blank=True, related_name='users'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='pharmacist')
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.username} ({self.pharmacy})"
