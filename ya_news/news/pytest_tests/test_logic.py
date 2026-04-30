import pytest
from django.test import TestCase


@pytest.mark.django_db
class TestLogic(TestCase):
    """Тесты логики."""

    def test_logic(self):
        """Логика работает."""
        pass
