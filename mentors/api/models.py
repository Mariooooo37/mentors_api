from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель кастомного пользователя"""

    phone = models.CharField(max_length=15, blank=True, null=True)
    mentor = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="mentees"
    )

    def __str__(self):
        return self.username
