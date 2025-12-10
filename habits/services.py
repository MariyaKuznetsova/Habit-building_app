import requests

from config import settings


def send_telegram_bot(chat_id, message):
    """Отправка напоминания о том, в какое время какие привычки необходимо выполнять."""
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    requests.get(f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage', params=params)





