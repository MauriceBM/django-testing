import pytest
from django.contrib.auth import get_user_model
from news.models import News

User = get_user_model()


@pytest.fixture
def author():
    """Создание пользователя-автора."""
    return User.objects.create(username='author')


@pytest.fixture
def news(author):
    """Создание тестовой новости."""
    return News.objects.create(
        title='Test',
        text='Text',
        author=author
    )
