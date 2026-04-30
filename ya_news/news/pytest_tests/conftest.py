import pytest
from django.contrib.auth import get_user_model
from news.models import News

User = get_user_model()


@pytest.fixture
def author(db):
    """Фикстура: пользователь-автор."""
    return User.objects.create_user(
        username='author',
        password='testpass123'
    )


@pytest.fixture
def news(db, author):
    """Фикстура: тестовая новость."""
    return News.objects.create(
        title='Test News',
        text='Test text',
        author=author
    )
