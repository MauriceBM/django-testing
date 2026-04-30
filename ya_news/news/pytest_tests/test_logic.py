import pytest
from django.urls import reverse
from news.models import Comment


@pytest.mark.django_db
def test_comment_created(author_client, news):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, {'text': 'OK'})
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 1
