from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicineViewSet, StockMovementViewSet

router = DefaultRouter()
router.register(r'medicines', MedicineViewSet, basename='medicine')
router.register(r'stock-movements', StockMovementViewSet, basename='stock-movement')

urlpatterns = [
    path('', include(router.urls)),
]
