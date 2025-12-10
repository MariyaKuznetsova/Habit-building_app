from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    validate_associated_habit,
    validate_period,
    validate_pleasant_habit,
    validate_reward,
    validate_time_complete,
)


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор по привычки"""

    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, attrs):
        associated_habit = attrs.get("associated_habit")
        reward = attrs.get("reward")
        time_complete = attrs.get("time_complete")
        pleasant_habit = attrs.get("pleasant_habit")
        period = attrs.get("period")
        validate_associated_habit(associated_habit, reward)
        validate_time_complete(time_complete)
        validate_pleasant_habit(associated_habit)
        validate_reward(associated_habit, pleasant_habit, reward)
        validate_period(period)
        return attrs
