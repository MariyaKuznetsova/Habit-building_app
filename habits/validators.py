from rest_framework.serializers import ValidationError


def validate_associated_habit(associated_habit, reward):
    """Валидация на исключение одновременный выбор связанной привычки и указания вознаграждения."""
    if associated_habit and reward:
        raise ValidationError("Нельзя в связанной привычке указывать вознаграждение!")
    elif not associated_habit and not reward:
        raise ValidationError("Нужно выбрать либо указать что связанная привычка или добавить вознаграждение!")


def validate_time_complete(time_complete):
    """Валидация на время выполнения должно быть не больше 120 секунд."""
    if time_complete > 120:
        raise ValidationError("Время выполнения должно быть не больше 120 секунд.")


def validate_pleasant_habit(associated_habit):
    """Валидация на связанные привычки могут попадать только привычки с признаком приятной привычки."""
    if associated_habit and associated_habit.pleasant_habit == False:
        raise ValidationError("В связанные привычки могут попадать только привычки с признаком приятной привычки.")


def validate_reward(associated_habit, pleasant_habit, reward):
    """Валидация на у приятной привычки не может быть вознаграждения или связанной привычки."""
    if pleasant_habit == True and (associated_habit or reward):
        raise ValidationError("Не может приятная привычка быть связанной привычкой или иметь вознаграждение!")


def validate_period(period):
    """Валидация на выполнение привычки"""
    if period > 7:
        raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")
