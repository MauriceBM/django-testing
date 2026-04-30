import pytest
from django.test import TestCase


@pytest.mark.django_db
class TestContent(TestCase):
    """Тесты контента."""

    def test_list(self):
        """Список работает."""
        pass
