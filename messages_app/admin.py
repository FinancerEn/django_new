from django.contrib import admin
from .models import Dialog
from typing import Any


@admin.register(Dialog)
class DialogAdmin(admin.ModelAdmin):
    list_display = ('get_participants', 'last_message', 'get_last_message_time')

    def get_participants(self, obj: Any) -> str:
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = "Участники"

    def get_last_message_time(self, obj: Any) -> str:
        return obj.last_message.timestamp.strftime('%d.%m.%Y %H:%M') if obj.last_message else "Нет сообщений"
    get_last_message_time.short_description = "Время последнего сообщения"
