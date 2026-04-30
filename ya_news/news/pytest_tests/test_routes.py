import pytest
from http import HTTPStatus
from django.urls import reverse


@pytest.mark.django_db
def test_home_status(client):
    response = client.get(reverse('news:home'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_detail_status(client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
