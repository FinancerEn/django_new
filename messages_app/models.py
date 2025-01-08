from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    # Текст сообщения
    content = models.TextField()
    # Время отправки
    timestamp = models.DateTimeField(auto_now_add=True)
    # Прочитано или нет
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"От {self.sender} к {self.receiver}: {self.content[:20]}"


class Dialog(models.Model):
    participants = models.ManyToManyField(User)
    last_message = models.ForeignKey('Message', null=True, blank=True, on_delete=models.SET_NULL)

    def user_is_participant(self, user):
        # Дополнительная проверка, является ли пользователь участником диалога.
        return self.participants.filter(id=user.id).exists()

    def __str__(self):
        return f"Диалог между {', '.join([user.username for user in self.participants.all()])}"
