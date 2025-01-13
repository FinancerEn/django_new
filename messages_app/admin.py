from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    # Столбцы для отображения
    list_display = ('get_sender', 'get_receiver', 'content', 'timestamp')
    search_fields = ['sender__username', 'receiver__username']  # Поиск по отправителю и получателю
    list_filter = ['timestamp']  # Фильтрация по дате
    list_per_page = 10  # Пагинация по 10 сообщений

    # Метод для отображения отправителя
    def get_sender(self, obj):
        return obj.sender.username
    get_sender.short_description = "Отправитель"

    # Метод для отображения получателя
    def get_receiver(self, obj):
        return obj.receiver.username
    get_receiver.short_description = "Получатель"

    # Метод для отображения сообщения
    def get_content(self, obj):
        return obj.content
    get_content.short_description = "Сообщение"

    # Метод для отображения даты и времени
    def get_timestamp(self, obj):
        return obj.timestamp
    get_timestamp.short_description = "Дата и время"
