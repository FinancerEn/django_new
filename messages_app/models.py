from django.db import models
from django.conf import settings
settings.AUTH_USER_MODEL
from django.core.exceptions import ValidationError
from django.conf import settings

'''Описание: Модель описывает сообщения между пользователями, включая отправителя,
получателя, текст, отметку времени, и статус "прочитано/не прочитано".'''


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="related_name", on_delete=models.CASCADE)
    # Текст сообщения
    content = models.TextField()
    # Время отправки
    timestamp = models.DateTimeField(auto_now_add=True)
    # Прочитано или нет
    is_read = models.BooleanField(default=False)

    def clean(self):
        if not self.content.strip():
            raise ValidationError("Поле сообщения не может быть пустым.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Проверяем валидацию перед сохранением
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['-timestamp']

    def __str__(self):
        return f"От {self.sender} к {self.receiver}: {self.content[:20]}"


class Dialog(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    last_message = models.ForeignKey('Message', null=True, blank=True, on_delete=models.SET_NULL)

    def user_is_participant(self, user):
        # Дополнительная проверка, является ли пользователь участником диалога.
        return self.participants.filter(id=user.id).exists()

    def __str__(self):
        # participants поле для связи участников с диалогами.
        participants = [user.username for user in self.participants.all()]
        return f"Диалог между {', '.join(participants[:5])}" + (' и других' if len(participants) > 5 else '')

    class Meta:
        verbose_name = "Диалог"
        verbose_name_plural = "Диалоги"
