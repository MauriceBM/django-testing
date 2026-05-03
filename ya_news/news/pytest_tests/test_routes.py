from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db

LOGIN_URL = reverse('users:login')
HOME_URL = reverse('news:home')


def test_home_availability_for_anonymous(client):
    """Главная страница доступна анонимному пользователю."""
    response = client.get(HOME_URL)
    assert response.status_code == HTTPStatus.OK


def test_news_detail_availability_for_anonymous(client, news):
    """Страница отдельной новости доступна анонимному пользователю."""
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('url_name', ['news:edit', 'news:delete'])
def test_comment_edit_delete_accessible_only_author(
    author_client, comment, url_name
):
    """Страницы ред. и удаления комментария доступны автору."""
    url = reverse(url_name, args=(comment.id,))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('url_name', ['news:edit', 'news:delete'])
def test_anonymous_redirected_to_login_for_comment_edit_delete(
    client, comment, url_name
):
    """Аноним перенаправляется sur логин pour ред./suppression."""
    url = reverse(url_name, args=(comment.id,))
    response = client.get(url)
    expected_url = f"{LOGIN_URL}?next={url}"
    assertRedirects(response, expected_url)


@pytest.mark.parametrize('url_name', ['news:edit', 'news:delete'])
def test_other_user_cannot_access_comment_edit_delete(
    not_author_client, comment, url_name
):
    """Autre utilisateur ne peut pas ред./supprimer les commentaires."""
    url = reverse(url_name, args=(comment.id,))
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_auth_pages_available_for_anonymous(client):
    """Pages d'auth доступны анонимным пользователям."""
    login_url = reverse('users:login')
    signup_url = reverse('users:signup')
    logout_url = reverse('users:logout')

    response_login = client.get(login_url)
    response_signup = client.get(signup_url)
    response_logout = client.post(logout_url)

    assert response_login.status_code == HTTPStatus.OK
    assert response_signup.status_code == HTTPStatus.OK
    assert response_logout.status_code in (HTTPStatus.OK, HTTPStatus.FOUND)
