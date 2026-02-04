from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPagination
from habits.serializers import HabitSerializer
from habits.tasks import send_telegram
from users.permissions import IsOwner


class HabitCreateAPIView(generics.CreateAPIView):
    """Контроллер по созданию привычки"""

    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        send_telegram.delay()


class HabitListAPIView(generics.ListAPIView):
    """Контроллер по выводу списка привычек"""

    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


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
