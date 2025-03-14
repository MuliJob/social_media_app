from django.http import JsonResponse

from rest_framework.decorators import api_view

from .models import Notification
from .serializers import NotificationSerializer


@api_view(['GET'])
def notifications(request):
    """gETTING NOTIFICAtions"""
    received_notifications = request.user.received_notifications.filter(is_read=False)
    serializer = NotificationSerializer(received_notifications, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def read_notification(request, pk):
    """Reading a notification"""
    notification = Notification.objects.filter(created_for=request.user).get(pk=pk)
    notification.is_read = True
    notification.save()

    return JsonResponse({'message': 'notification read'})
