import pytest
from django.test import TestCase


@pytest.mark.django_db
class TestRoutes(TestCase):
    """Тесты маршрутов."""

    def test_home(self):
        """Главная доступна."""
        pass
