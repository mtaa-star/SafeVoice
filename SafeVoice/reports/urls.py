from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_violence, name='report_violence'),
    path('success/', views.report_success, name='report_success'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('edit-report/<int:pk>/', views.edit_report, name='edit_report'),
    path('delete-report/<int:pk>/', views.delete_report, name='delete_report'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'), 
]