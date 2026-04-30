import pytest
from django.urls import reverse
from news.models import Comment


@pytest.mark.django_db
def test_comment_creation(author_client, news):
    """Авторизованный пользователь может создать комментарий."""
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, {'text': 'Test comment'})
    assert response.status_code == 302
    assert Comment.objects.count() == 1
