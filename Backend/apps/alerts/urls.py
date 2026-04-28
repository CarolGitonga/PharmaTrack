from django.urls import path
from .views import AlertLogListView, TestSMSView

urlpatterns = [
    path('alerts/logs/', AlertLogListView.as_view(), name='alert-logs'),
    path('alerts/test-sms/', TestSMSView.as_view(), name='test-sms'),
]
