# Файл связанный с админкой, вкладка "Приложение сообщений"
from django.apps import AppConfig


class MessagesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messages_app'
    verbose_name = "Приложение сообщений"  # Название приложения в админке
