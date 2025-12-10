from django.db import models

from users.models import User


class Habit(models.Model):
    """Класс привычки"""

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Владелец привычки",
    )
    place = models.CharField(max_length=150, verbose_name="Место привычки")
    time = models.TimeField(verbose_name="Время выполнения привычки")
    description = models.CharField(max_length=150, verbose_name="Описание привычки")
    pleasant_habit = models.BooleanField(verbose_name="Полезная привычка")
    associated_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank = True,
        null = True,
        verbose_name="Связанная привычка",
    )
    period = models.IntegerField(verbose_name="Периодичность выполнения привычки в днях")
    reward = models.CharField(max_length=150, blank=True, null=True, verbose_name="Вознаграждение за выполнение привычки")
    time_complete = models.IntegerField(verbose_name="Время на выполнение привычки в секундах")
    public = models.BooleanField(verbose_name="Признак публичности")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["owner", "place", "time", "description", "pleasant_habit", "associated_habit", "period", "time_complete", "public"]

    def __str__(self):
        return self.owner


