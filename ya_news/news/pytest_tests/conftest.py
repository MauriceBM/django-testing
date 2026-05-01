import pytest
from django.contrib.auth import get_user_model
from django.test.client import Client

from news.models import News, Comment

User = get_user_model()

BAD_WORDS = ['запрещённое_слово', 'spam', 'offensive']


@pytest.fixture
def author(db):
    """Фикстура: пользователь-автор."""
    return User.objects.create_user(
        username='author', password='pass123'
    )


@pytest.fixture
def not_author(db):
    """Фикстура: другой пользователь (не автор)."""
    return User.objects.create_user(
        username='not_author', password='pass123'
    )


@pytest.fixture
def author_client(author):
    """Клиент, авторизованный как автор."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    """Клиент, авторизованный как другой пользователь."""
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(db, author):
    """Одна новость."""
    return News.objects.create(
        title='Test News', text='Text', author=author
    )


@pytest.fixture
def many_news(db, author):
    """11 новостей для проверки лимита на главной."""
    all_news = [
        News(title=f'News {i}', text='Text', author=author)
        for i in range(11)
    ]
    return News.objects.bulk_create(all_news)


@pytest.fixture
def comment(db, author, news):
    """Один комментарий, созданный автором."""
    return Comment.objects.create(
        text='Comment text', author=author, news=news
    )


@pytest.fixture
def news_with_comments(db, author, not_author, news):
    """Новость с несколькими комментариями разной даты."""
    comments_data = [
        ('First', author, '2024-01-01 10:00:00'),
        ('Second', not_author, '2024-01-02 10:00:00'),
        ('Third', author, '2024-01-03 10:00:00'),
    ]
    for text, user, date in comments_data:
        comment = Comment.objects.create(
            text=text, author=user, news=news
        )
        comment.created = date
        comment.save()
    return news
