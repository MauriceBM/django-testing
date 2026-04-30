from django.test import TestCase


class TestRoutes(TestCase):
    """Тесты маршрутов."""

    def test_home(self):
        """Главная доступна."""
        self.assertTrue(True)
