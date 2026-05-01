from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db

LOGIN_URL = reverse('users:login')


def test_home_availability_for_anonymous(client):
    """Главная страница доступна анонимному пользователю."""
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_news_detail_availability_for_anonymous(client, news):
    """Страница отдельной новости доступна анонимному пользователю."""
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_comment_edit_delete_accessible_only_author(
    author_client, comment
):
    """Страницы ред. и удаления комментария доступны автору."""
    edit_url = reverse('news:edit', args=(comment.id,))
    delete_url = reverse('news:delete', args=(comment.id,))
    response_edit = author_client.get(edit_url)
    response_delete = author_client.get(delete_url)
    assert response_edit.status_code == HTTPStatus.OK
    assert response_delete.status_code == HTTPStatus.OK


def test_anonymous_redirected_to_login_for_comment_edit_delete(
    client, comment
):
    """Аноним перенаправляется на логин при попытке ред./удалить коммент."""
    edit_url = reverse('news:edit', args=(comment.id,))
    delete_url = reverse('news:delete', args=(comment.id,))
    for url in (edit_url, delete_url):
        response = client.get(url)
        expected_url = f'{LOGIN_URL}?next={url}'
        assertRedirects(response, expected_url)


def test_other_user_cannot_access_comment_edit_delete(
    not_author_client, comment
):
    """Авториз. пользователь не может ред./удалить чужие коммент. (404)."""
    edit_url = reverse('news:edit', args=(comment.id,))
    delete_url = reverse('news:delete', args=(comment.id,))
    for url in (edit_url, delete_url):
        response = not_author_client.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND


def test_auth_pages_available_for_anonymous(client):
    """Стр. регистрации, входа и выхода доступны анонимным пользователям."""
    login_url = reverse('users:login')
    signup_url = reverse('users:signup')
    logout_url = reverse('users:logout')
    response_login = client.get(login_url)
    response_signup = client.get(signup_url)
    response_logout = client.post(logout_url)
    assert response_login.status_code == HTTPStatus.OK
    assert response_signup.status_code == HTTPStatus.OK
    assert response_logout.status_code in (HTTPStatus.OK, HTTPStatus.FOUND)
