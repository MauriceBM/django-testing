import pytest
from django.test.client import Client
from notes.models import Note


@pytest.fixture
def author(django_user_model):
    """Создание пользователя-автора заметок."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    """Создание обычного пользователя (не автора)."""
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    """Клиент, авторизованный как автор заметки."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    """Клиент, авторизованный как обычный пользователь."""
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def note(author):
    """Создание тестовой заметки для автора."""
    return Note.objects.create(
        title='Заголовок',
        text='Текст заметки',
        slug='note-slug',
        author=author,
    )


@pytest.fixture
def slug_for_args(note):
    """Возвращает slug заметки в виде кортежа для reverse()."""
    return (note.slug,)


@pytest.fixture
def form_data():
    """Словарь с данными формы для создания заметки."""
    return {
        'title': 'Новый заголовок',
        'text': 'Новый текст',
        'slug': 'new-slug'
    }
