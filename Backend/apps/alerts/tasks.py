from celery import shared_task
from django.utils import timezone


@shared_task
def run_daily_alert_checks():
    from apps.inventory.models import Medicine
    from apps.accounts.models import Pharmacy
    from .services import SMSAlertService

    sms = SMSAlertService()
    today = timezone.now().date()

    for pharmacy in Pharmacy.objects.filter(is_active=True):
        medicines = Medicine.objects.filter(pharmacy=pharmacy, is_active=True)

        for medicine in medicines:
            if medicine.is_low_stock:
                sms.send_low_stock_alert(pharmacy, medicine)

            days = medicine.days_to_expiry
            if days in [60, 30, 7]:
                sms.send_expiry_alert(pharmacy, medicine, days)

    return f"Alert checks completed for {Pharmacy.objects.filter(is_active=True).count()} pharmacies."
