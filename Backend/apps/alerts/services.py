import africastalking
from django.conf import settings
from .models import AlertLog


class SMSAlertService:
    def __init__(self):
        africastalking.initialize(
            username=settings.AT_USERNAME,
            api_key=settings.AT_API_KEY
        )
        self.sms = africastalking.SMS

    def send_low_stock_alert(self, pharmacy, medicine):
        message = (
            f"[PharmaTrack] LOW STOCK ALERT\n"
            f"Medicine: {medicine.name}\n"
            f"Current stock: {medicine.quantity} {medicine.unit}\n"
            f"Minimum level: {medicine.minimum_quantity} {medicine.unit}\n"
            f"Please reorder soon."
        )
        return self._send(pharmacy, medicine, 'LOW_STOCK', message)

    def send_expiry_alert(self, pharmacy, medicine, days_remaining):
        if days_remaining <= 0:
            alert_type = 'EXPIRED'
        elif days_remaining <= 30:
            alert_type = 'EXPIRING_30'
        else:
            alert_type = 'EXPIRING_60'

        message = (
            f"[PharmaTrack] EXPIRY ALERT\n"
            f"Medicine: {medicine.name}\n"
            f"Batch: {medicine.batch_number}\n"
            f"Expires in: {days_remaining} days ({medicine.expiry_date})\n"
            f"Quantity: {medicine.quantity} {medicine.unit}"
        )
        return self._send(pharmacy, medicine, alert_type, message)

    def send_test_sms(self, pharmacy):
        message = (
            f"[PharmaTrack] Test SMS\n"
            f"Hello {pharmacy.owner_name}, your SMS alerts are working correctly.\n"
            f"Pharmacy: {pharmacy.name}"
        )
        try:
            response = self.sms.send(message, [pharmacy.phone])
            return {'success': True, 'response': response}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _send(self, pharmacy, medicine, alert_type, message):
        success = True
        try:
            self.sms.send(message, [pharmacy.phone])
        except Exception as e:
            success = False

        AlertLog.objects.create(
            pharmacy=pharmacy,
            medicine=medicine,
            alert_type=alert_type,
            message=message,
            sent_to=pharmacy.phone,
            was_successful=success,
        )
        return success
