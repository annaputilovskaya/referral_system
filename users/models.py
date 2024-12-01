from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """
    Модель пользователя.
    """

    username = None
    password = models.CharField(max_length=128, **NULLABLE, verbose_name="Пароль")
    phone = PhoneNumberField(unique=True, verbose_name="Телефон")
    verification_code = models.CharField(
        max_length=4, **NULLABLE, verbose_name="Код авторизации"
    )
    invite_code = models.CharField(
        max_length=6, unique=True, **NULLABLE, verbose_name="Код приглашения"
    )
    invited_by = models.ForeignKey(
        "self",
        **NULLABLE,
        on_delete=models.SET_NULL,
        verbose_name="Приглашен пользователем",
        related_name="referrals",
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.phone}"
