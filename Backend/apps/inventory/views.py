from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import F
from django.utils import timezone
from datetime import timedelta
from .models import Medicine, StockMovement
from .serializers import MedicineSerializer, StockMovementSerializer


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


class StockMovementViewSet(viewsets.ModelViewSet):
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        qs = StockMovement.objects.filter(pharmacy=self.request.user.pharmacy)
        medicine_id = self.request.query_params.get('medicine')
        if medicine_id:
            qs = qs.filter(medicine_id=medicine_id)
        return qs.order_by('-date')

    def perform_create(self, serializer):
        medicine = serializer.validated_data['medicine']
        movement_type = serializer.validated_data['movement_type']
        quantity = serializer.validated_data['quantity']

        if movement_type in ['IN', 'ADJUSTMENT']:
            medicine.quantity += quantity
        elif movement_type in ['OUT', 'EXPIRED']:
            medicine.quantity -= quantity

        medicine.save()
        serializer.save(
            pharmacy=self.request.user.pharmacy,
            performed_by=self.request.user
        )
