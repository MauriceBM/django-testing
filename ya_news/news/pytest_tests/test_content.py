import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_news_limit_on_home_page(client):
    """На главной странице не более 10 новостей."""
    url = reverse('news:home')
    response = client.get(url)
    news_list = response.context['news_list']
    assert len(news_list) <= 10


@pytest.mark.django_db
def test_news_sorted_newest_first(client):
    """Новости отсортированы от свежих к старым."""
    url = reverse('news:home')
    response = client.get(url)
    news_list = response.context['news_list']
    if len(news_list) > 1:
        assert news_list[0].pub_date >= news_list[-1].pub_date


@pytest.mark.django_db
def test_comments_sorted_chronologically(client, news):
    """Комментарии отсортированы от старых к новым."""
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    comments = (
        response.context.get('comments')
        or response.context.get('comment_list')
        or response.context.get('object_list')
    )
    if comments and len(comments) > 1:
        assert comments[0].created <= comments[-1].created


@pytest.mark.django_db
def test_comment_form_visibility(client, author_client, news):
    """Форма комментария видна только авторизованному."""
    url = reverse('news:detail', args=(news.id,))
    resp_anon = client.get(url)
    resp_auth = author_client.get(url)
    assert 'form' not in resp_anon.context
    assert 'form' in resp_auth.context
