from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, F
from django.utils import timezone
from datetime import timedelta
from apps.inventory.models import Medicine


class SummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pharmacy = request.user.pharmacy
        today = timezone.now().date()
        threshold = today + timedelta(days=60)

        medicines = Medicine.objects.filter(pharmacy=pharmacy, is_active=True)

        total_medicines = medicines.count()
        low_stock_count = medicines.filter(quantity__lte=F('minimum_quantity')).count()
        expiring_soon_count = medicines.filter(expiry_date__gt=today, expiry_date__lte=threshold).count()
        expired_count = medicines.filter(expiry_date__lte=today).count()

        total_stock_value = medicines.aggregate(
            value=Sum(F('quantity') * F('buying_price'))
        )['value'] or 0

        return Response({
            'total_medicines': total_medicines,
            'low_stock_count': low_stock_count,
            'expiring_soon_count': expiring_soon_count,
            'expired_count': expired_count,
            'total_stock_value': round(total_stock_value, 2),
        })
