import pytest
from http import HTTPStatus
from django.urls import reverse


@pytest.mark.django_db
def test_home_page_accessible(client):
    """Главная страница доступна."""
    response = client.get(reverse('news:home'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_detail_page_accessible(client, news):
    """Страница новости доступна."""
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
