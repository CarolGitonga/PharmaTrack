from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import F
from django.utils import timezone
from datetime import timedelta
from .models import Medicine
from .serializers import MedicineSerializer


class MedicineViewSet(viewsets.ModelViewSet):
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Medicine.objects.filter(
            pharmacy=self.request.user.pharmacy,
            is_active=True
        )

    def perform_create(self, serializer):
        serializer.save(pharmacy=self.request.user.pharmacy)

    def destroy(self, request, *args, **kwargs):
        medicine = self.get_object()
        medicine.is_active = False
        medicine.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock(self, request):
        qs = self.get_queryset().filter(quantity__lte=F('minimum_quantity'))
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def expiring(self, request):
        today = timezone.now().date()
        threshold = today + timedelta(days=60)
        qs = self.get_queryset().filter(expiry_date__gt=today, expiry_date__lte=threshold)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def expired(self, request):
        today = timezone.now().date()
        qs = self.get_queryset().filter(expiry_date__lte=today)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
