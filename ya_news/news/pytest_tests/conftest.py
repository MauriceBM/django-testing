import pytest
from django.test.client import Client


@pytest.fixture
def author(django_user_model):
    """Création d'un utilisateur auteur."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    """Création d'un utilisateur non-auteur."""
    return django_user_model.objects.create(username='НеАвтор')


@pytest.fixture
def author_client(author):
    """Client authentifié en tant qu'auteur."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    """Client authentifié en tant qu'utilisateur standard."""
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(author):
    """Création d'une news de test."""
    from news.models import News
    return News.objects.create(
        title='Тестовая новость',
        text='Текст новости',
        author=author
    )


@pytest.fixture
def comment(author, news):
    """Création d'un commentaire de test."""
    from news.models import Comment
    return Comment.objects.create(
        text='Тестовый комментарий',
        author=author,
        news=news
    )


@pytest.fixture
def form_data():
    """Données pour le formulaire de commentaire."""
    return {'text': 'Новый комментарий'}
