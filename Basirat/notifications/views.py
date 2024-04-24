from django.shortcuts import render


# Create your views here.
def notifications(request):
    return render(request, 'notifications/notifications.html')


def delete_notification(request):
    return render(request, 'notifications/delete_notification.html')


def add_notification(request):
    return render(request, 'notifications/add_notification.html')
