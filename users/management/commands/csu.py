from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда создания администратора (суперпользователя).
    """

    def handle(self, *args, **kwargs):
        user = User.objects.create(phone="+79001231212")
        user.set_password("admin")
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
