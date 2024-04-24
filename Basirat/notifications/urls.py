from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notifications, name='notifications'),
    path('add/', views.add_notification, name='add_notification'),
    path('delete/', views.delete_notification, name='delete_notification'),
]