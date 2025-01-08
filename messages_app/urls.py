from django.urls import path
from . import views

app_name = 'messages_app'

urlpatterns = [
    path('dialogs/', views.dialogs_list, name='dialogs_list'),
    path('dialogs/<int:dialog_id>/', views.dialog_detail, name='dialog_detail'),
    path('dialogs/<int:dialog_id>/send/', views.send_message, name='send_message'),
]
