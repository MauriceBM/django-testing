import pytest
from django.contrib.auth import get_user_model
from news.models import News

User = get_user_model()


@pytest.fixture
def author(db):
    return User.objects.create_user(
        username='author',
        password='pass123'
    )


@pytest.fixture
def news(db, author):
    return News.objects.create(
        title='Test',
        text='Text',
        author=author
    )
