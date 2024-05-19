from django.shortcuts import render
from .models import Message


# Create your views here.
def notifications(request):
    messages = Message.objects.filter(group__students__user=request.user)
    return render(request, 'notifications/notifications.html', {'messages': messages})


def delete_notification(request):
    return render(request, 'notifications/delete_notification.html')


def add_notification(request):
    return render(request, 'notifications/add_notification.html')
