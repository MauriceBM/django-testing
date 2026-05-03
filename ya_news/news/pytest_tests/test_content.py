import pytest
from django.conf import settings
from django.urls import reverse

from news.pytest_tests.urls import HOME_URL, DETAIL_URL_NAME

pytestmark = pytest.mark.django_db

FORM_CONTEXT_KEY = 'form'


def test_news_limit_on_home_page(client, many_news):
    """Количество новостей на главной странице не превышает лимит."""
    expected_max = settings.NEWS_COUNT_ON_HOME_PAGE

    response = client.get(HOME_URL)
    news_list = response.context['object_list']

    assert news_list.count() <= expected_max


def test_news_ordered_from_newest_to_oldest(client, many_news):
    """Новости отсортированы по дате убывания."""
    response = client.get(HOME_URL)
    news_list = list(response.context['object_list'])

    assert all(
        news_list[i].date >= news_list[i + 1].date
        for i in range(len(news_list) - 1)
    )


def test_comments_ordered_chronologically(client, news_with_comments):
    """Комментарии отсортированы по дате возрастания."""
    news = news_with_comments

    comments = list(news.comment_set.all())

    assert all(
        comments[i].created <= comments[i + 1].created
        for i in range(len(comments) - 1)
    )


def test_comment_form_hidden_for_anonymous(client, news):
    """Форма комментария скрыта для анонимных пользователей."""
    url = reverse(DETAIL_URL_NAME, args=(news.id,))

    response = client.get(url)

    assert FORM_CONTEXT_KEY not in response.context


def test_comment_form_visible_for_authenticated(author_client, news):
    """Форма комментария видна авторизованным пользователям."""
    url = reverse(DETAIL_URL_NAME, args=(news.id,))

    response = author_client.get(url)

    assert FORM_CONTEXT_KEY in response.context
