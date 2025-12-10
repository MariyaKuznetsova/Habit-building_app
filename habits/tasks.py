from datetime import timedelta, timezone


from celery import shared_task

from habits.models import Habit

from users.models import User
from habits.services import send_telegram_bot


@shared_task
def send_telegram(email):
    """Отправка напоминания о том, в какое время какие привычки необходимо выполнять."""
    habit = Habit.objects.get(owner=email)
    message = habit.description
    time = habit.time
    chat_id = User.objects.get(email=email)
    print(chat_id)
    print(time)
    if time <= timezone.now() < time + timedelta(minutes=1):
        send_telegram_bot(message, chat_id)





