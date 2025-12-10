from django.db.migrations import serializer
from rest_framework import generics, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from habits.models import Habit
from habits.paginators import MyPagination
from habits.serializers import HabitSerializer
from habits.tasks import send_telegram
from users.permissions import IsOwner


class HabitCreateAPIView(generics.CreateAPIView):
    """Контроллер по созданию привычки"""

    serializer_class = HabitSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        # habit = serializer.save()
        # send_telegram.delay(habit.owner)

    def get_period_for_task(self):
        """Функция для получения периодичности выполнения привычки в днях"""
        habit = Habit.objects.get(owner=self.request.user)
        period = habit.period
        return period


class HabitListAPIView(generics.ListAPIView):
    """Контроллер по выводу списка привычек"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    pagination_class = MyPagination


class HabitPublicListAPIView(generics.ListAPIView):
    """Контроллер по выводу списка публичных привычек"""

    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        return Habit.objects.filter(public=True)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер по выводу привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Контроллер по редактированию привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Контроллер по удаления привычки"""

    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    queryset = Habit.objects.all()

