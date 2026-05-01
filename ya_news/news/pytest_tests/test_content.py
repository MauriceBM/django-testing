import pytest
from django.conf import settings
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_news_limit_on_home_page(client, many_news):
    """Количество новостей sur главной странице — не более 10."""
    url = reverse('news:home')

    response = client.get(url)

    news_list = response.context['object_list']
    assert news_list.count() <= settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_ordered_from_newest_to_oldest(client, many_news):
    """Новости отсортированы par date décroissante."""
    url = reverse('news:home')

    response = client.get(url)

    news_list = list(response.context['object_list'])
    for i in range(len(news_list) - 1):
        assert news_list[i].date >= news_list[i + 1].date


def test_comments_ordered_chronologically(client, news_with_comments):
    """Комментарии на стр. новости отсортированы par date croissante."""
    news = news_with_comments

    comments = news.comment_set.all()

    for i in range(len(comments) - 1):
        assert comments[i].created <= comments[i + 1].created


def test_comment_form_hidden_for_anonymous(client, news):
    """Анонимному пользователю не видна форма отправки комментария."""
    url = reverse('news:detail', args=(news.id,))

    response = client.get(url)

    assert 'form' not in response.context


def test_comment_form_visible_for_authenticated(author_client, news):
    """Авторизованному пользователю видна форма отправки комментария."""
    url = reverse('news:detail', args=(news.id,))

    response = author_client.get(url)

    assert 'form' in response.context
