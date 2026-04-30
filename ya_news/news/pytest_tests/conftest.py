import pytest
from django.contrib.auth import get_user_model
from django.test.client import Client

from news.models import News, Comment

User = get_user_model()


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
    all_news = []
    for i in range(11):
        news = News(title=f'News {i}', text='Text', author=author)
        all_news.append(news)
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
    c1 = Comment.objects.create(text='First', author=author, news=news)
    c1.created = '2024-01-01 10:00:00'
    c1.save()
    c2 = Comment.objects.create(text='Second', author=not_author, news=news)
    c2.created = '2024-01-02 10:00:00'
    c2.save()
    c3 = Comment.objects.create(text='Third', author=author, news=news)
    c3.created = '2024-01-03 10:00:00'
    c3.save()
    return news


@pytest.fixture
def bad_words_data():
    """Список запрещённых слов (берётся из настроек проекта)."""
    from news.forms import BAD_WORDS
    return BAD_WORDS
