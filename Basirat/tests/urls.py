from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('create/', views.create_test_page, name='create_test_page'),
    path('create_test/', views.create_test, name='create_test'),
    path('edit/<int:test_id>/', views.edit_test_page, name='edit_test_page'),
    path('edit_test/', views.edit_test, name='edit_test'),
    path('delete_test/', views.delete_test, name='delete_test'),
    path('create_question/', views.create_question, name='create_question'),
    path('deactivate/', views.deactivate_test_endpoint, name='deactivate_test_endpoint'),
    path('delete_question/', views.delete_question, name='delete_question'),
    path('take_test/<int:test_id>/', views.take_test, name='take_test'),
    path('submit_test/<int:test_id>/', views.submit_answers, name='submit_answers'),
    path('test_result/<int:test_id>/', views.test_result, name='test_result'),
    path('check_test/<int:unchecked_test_id>/', views.check_test, name='check_test'),
]
