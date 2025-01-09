from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
settings.AUTH_USER_MODEL


class CustomUser(AbstractUser):
    user: models.OneToOneField = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone: models.CharField = models.CharField(max_length=15, verbose_name="Телефон")
    address: models.TextField = models.TextField(verbose_name="Адрес")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    def __str__(self) -> str:
        return self.user.username
