import pytest
from django.urls import reverse
from news.models import Comment


@pytest.mark.django_db
def test_comment_created_on_post(author_client, news):
    """Комментарий создаётся при валидном POST."""
    url = reverse('news:detail', args=(news.id,))
    data = {'text': 'Valid comment'}
    response = author_client.post(url, data)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_bad_word_blocked(author_client, news):
    """Комментарий с запрещённым словом не создаётся."""
    url = reverse('news:detail', args=(news.id,))
    data = {'text': 'запрещённое_слово'}
    response = author_client.post(url, data)
    assert Comment.objects.count() == 0
