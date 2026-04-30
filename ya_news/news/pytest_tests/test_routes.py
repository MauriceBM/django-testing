import pytest
from http import HTTPStatus
from django.urls import reverse


@pytest.mark.django_db
def test_home_page_status(client):
    """Главная страница возвращает 200."""
    response = client.get(reverse('news:home'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_detail_page_status(client, news):
    """Страница новости возвращает 200."""
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
