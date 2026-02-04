from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Тест CRUD привычек."""

    def setUp(self):
        """Создание тестового пользователя для авторизации."""
        self.user = User.objects.create(email="admin2025@example.com")

        self.habit = Habit.objects.create(
            owner=self.user,
            place="Дома",
            description="Выпить стакан воды",
            time="9:00",
            pleasant_habit="False",
            period=1,
            reward="Похвалить себя, ведь весь твой организм заработал",
            time_complete=60,
            public="False",
        )

        self.client.force_authenticate(user=self.user)

    def test_retrieve_habit(self):
        """Тест вывод привычки."""

        url = reverse("habits:habit_detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("description"), self.habit.description)

    @patch('habits.tasks.send_telegram.delay')  # Мокаем задачу Celery
    def test_create_habit(self, mock_send_telegram):
        """Тест создания привычки."""
        mock_send_telegram.return_value = None  # Заглушка для Celery задачи

        url = reverse("habits:habit_create")
        data = {
            "owner": self.user.id,  # Используй ID созданного пользователя
            "place": "Дома",
            "description": "Выпить стакан воды",
            "time": "0:00",
            "pleasant_habit": "False",
            "period": 1,
            "reward": "Похвалить себя, ведь весь твой организм заработал",
            "time_complete": 60,
            "public": "False",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

        # Проверяем, что задача была вызвана
        mock_send_telegram.assert_called_once()

    def test_update_habit(self):
        """Тест обновления привычки."""
        url = reverse("habits:habit_update", args=(self.habit.pk,))
        data = {
            "period": 1,
            "pleasant_habit": "False",
            "reward": "Похвалить себя, ведь весь твой организм заработал",
            "time_complete": 60,
            "public": "True",
        }

        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("public"), True)

    def test_delete_habit(self):
        """Тест удаления привычки."""
        url = reverse("habits:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)
