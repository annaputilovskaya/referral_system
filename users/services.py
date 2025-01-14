import time
import string
from random import randint, sample


def send_sms(phone_number):
    """
    Имитирует отправку смс с 4-значным числовым кодом авторизации.
    """
    code = str(randint(0, 9999)).rjust(4, "0")
    time.sleep(2)
    print(f"Отправлено SMS на {phone_number} с кодом: {code}")
    return code


def generate_invite_code():
    """
    Генерирует случайный 6-значный инвайт-код из букв, цифр и спецсимволов.
    """
    return "".join(sample(string.digits + string.ascii_letters + string.punctuation, 6))
