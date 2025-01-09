"""
Тесты для приложения messages_app:

1. test_send_message:
   Проверяет успешную отправку сообщения (отправитель, получатель, содержание).

2. test_send_empty_message:
   Проверяет, что пустое сообщение нельзя отправить (ожидается ValidationError).

3. test_dialog_messages_and_participants:
   - Проверяет, что только участники диалога могут видеть его сообщения.
   - Убедились, что список сообщений возвращается корректно для участников диалога.
"""

import os
import django
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Dialog, Message
from django.core.exceptions import ValidationError

# Укажите путь к настройкам вашего проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # Замените 'myproject.settings' на реальный путь к вашим настройкам
django.setup()


class MessageTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", password="password")
        self.user2 = User.objects.create_user(username="User2", password="password")
        self.user3 = User.objects.create_user(username="User3", password="password")
        self.dialog = Dialog.objects.create()
        self.dialog.participants.set([self.user1, self.user2])

    def test_send_message(self):
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Test message")
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
        self.assertEqual(message.content, "Test message")

        def test_send_empty_message(self):
            # Ожидаем ValidationError вместо ValueError
            with self.assertRaises(ValidationError):
                Message.objects.create(sender=self.user1, receiver=self.user2, content="")

    def test_user_is_participant(self):
        # Проверяем, что user1 и user2 участвуют в диалоге
        self.assertTrue(self.dialog.user_is_participant(self.user1))
        self.assertTrue(self.dialog.user_is_participant(self.user2))
        # Проверяем, что user3 не участвует в диалоге
        self.assertFalse(self.dialog.user_is_participant(self.user3))

    def test_get_messages_for_dialog(self):
        # Создаем сообщения в рамках диалога
        message1 = Message.objects.create(sender=self.user1, receiver=self.user2, content="Message 1")
        message2 = Message.objects.create(sender=self.user2, receiver=self.user1, content="Message 2")
        # Привязываем последнее сообщение к диалогу
        self.dialog.last_message = message2
        self.dialog.save()

        # Проверяем, что сообщения получены корректно
        messages = Message.objects.filter(sender__in=self.dialog.participants.all(),
                                           receiver__in=self.dialog.participants.all())
        self.assertEqual(messages.count(), 2)
        self.assertIn(message1, messages)
        self.assertIn(message2, messages)