from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from news.pytest_tests.urls import (
    HOME_URL,
    LOGIN_URL,
    SIGNUP_URL,
    LOGOUT_URL,
    DETAIL_URL_NAME,
)

pytestmark = pytest.mark.django_db

COMMENT_ACTION_URLS = ('news:edit', 'news:delete')
AUTH_GET_URLS = ('users:login', 'users:signup')


def test_home_availability_for_anonymous(client):
    """Главная страница доступна анонимному пользователю."""
    response = client.get(HOME_URL)

    assert response.status_code == HTTPStatus.OK


def test_news_detail_availability_for_anonymous(client, news):
    """Страница отдельной новости доступна анонимному пользователю."""
    url = reverse(DETAIL_URL_NAME, args=(news.id,))

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('url_name', COMMENT_ACTION_URLS)
def test_comment_edit_delete_accessible_only_author(
    author_client, comment, url_name
):
    """Страницы редактирования и удаления доступны автору комментария."""
    url = reverse(url_name, args=(comment.id,))

    response = author_client.get(url)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('url_name', COMMENT_ACTION_URLS)
def test_anonymous_redirected_to_login_for_comment_edit_delete(
    client, comment, url_name
):
    """Аноним перенаправляется на вход при доступе к ред./удалению."""
    url = reverse(url_name, args=(comment.id,))

    response = client.get(url)

    expected_url = f"{LOGIN_URL}?next={url}"
    assertRedirects(response, expected_url)


@pytest.mark.parametrize('url_name', COMMENT_ACTION_URLS)
def test_other_user_cannot_access_comment_edit_delete(
    not_author_client, comment, url_name
):
    """Другой пользователь не может получить доступ к ред./удалению."""
    url = reverse(url_name, args=(comment.id,))

    response = not_author_client.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize('url_name', AUTH_GET_URLS)
def test_auth_get_pages_available_for_anonymous(client, url_name):
    """Страницы входа и регистрации доступны анонимам (GET)."""
    url = reverse(url_name)

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK


def test_logout_page_available_for_anonymous(client):
    """Страница выхода доступна анонимам (POST)."""
    response = client.post(LOGOUT_URL)

    assert response.status_code in (HTTPStatus.OK, HTTPStatus.FOUND)
