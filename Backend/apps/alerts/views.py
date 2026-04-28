from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import AlertLog
from .serializers import AlertLogSerializer
from .services import SMSAlertService


class AlertLogListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = AlertLog.objects.filter(
            pharmacy=request.user.pharmacy
        ).order_by('-sent_at')[:50]
        serializer = AlertLogSerializer(logs, many=True)
        return Response(serializer.data)


class TestSMSView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pharmacy = request.user.pharmacy
        if not pharmacy.phone:
            return Response(
                {'error': 'No phone number set for this pharmacy.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        sms = SMSAlertService()
        result = sms.send_test_sms(pharmacy)

        if result['success']:
            return Response({'message': f'Test SMS sent to {pharmacy.phone}.'})
        return Response(
            {'error': 'Failed to send SMS.', 'detail': result.get('error')},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
