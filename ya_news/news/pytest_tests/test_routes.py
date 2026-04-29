import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture as lf


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('news:home', 'news:detail')
)
def test_pages_for_anonymous_user(client, name, news):
    """Главная и страница новости доступны анониму."""
    if name == 'news:detail':
        url = reverse(name, args=(news.id,))
    else:
        url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lf('author_client'), HTTPStatus.OK),
        (lf('not_author_client'), HTTPStatus.NOT_FOUND),
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_comment_pages_for_author_vs_other(
    parametrized_client, name, comment, expected_status
):
    """Автор видит страницы редактирования/удаления, другие — 404."""
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_anonymous_redirect_to_login(client, comment):
    """Аноним перенаправляется на логин при доступе к комментарию."""
    url = reverse('news:edit', args=(comment.id,))
    response = client.get(url)
    login_url = reverse('users:login')
    assert response.status_code == HTTPStatus.FOUND
    assert login_url in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('users:login', 'users:signup', 'users:logout')
)
def test_auth_pages_for_anonymous_user(client, name):
    """Страницы авторизации доступны анонимному пользователю."""
    url = reverse(name)
    if name == 'users:logout':
        response = client.post(url)
    else:
        response = client.get(url)
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.FOUND)
