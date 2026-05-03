from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note

User = get_user_model()

SLUG_ERROR_MSG = (
    'test - такой slug уже существует, '
    'придумайте уникальное значение!'
)


def create_test_user(username, password='pass123'):
    """Создать тестового пользователя."""
    return User.objects.create_user(
        username=username, password=password
    )


def create_test_note(title, text, slug, author):
    """Создать тестовую заметку."""
    return Note.objects.create(
        title=title, text=text, slug=slug, author=author
    )


def get_logged_client(user):
    """Вернуть клиент, авторизованный как указанный пользователь."""
    client = Client()
    client.force_login(user)
    return client


class BaseTest(TestCase):
    """Базовый класс pour les tests avec données et clients communs."""

    @classmethod
    def setUpTestData(cls):
        """Création des données de test communes."""
        cls.author = create_test_user('author')
        cls.other_user = create_test_user('other')
        cls.note = create_test_note(
            'Test', 'Text', 'test', cls.author
        )
        cls.other_note = create_test_note(
            'Other', 'Other text', 'other', cls.other_user
        )
        cls.author_client = get_logged_client(cls.author)
        cls.other_client = get_logged_client(cls.other_user)
