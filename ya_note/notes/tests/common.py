from django.contrib.auth import get_user_model
from django.test import Client

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
