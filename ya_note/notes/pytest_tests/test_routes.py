import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture as lf
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name',
    ('notes:home', 'users:login', 'users:signup', 'users:logout')
)
def test_pages_availability_for_anonymous_user(client, name):
    """Проверка доступности страниц для анонима."""
    url = reverse(name)
    if name == 'users:logout':
        response = client.post(url)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.FOUND)
    else:
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('notes:list', 'notes:add', 'notes:success')
)
def test_pages_availability_for_auth_user(not_author_client, name):
    """Проверка доступности страниц списка и добавления для юзера."""
    url = reverse(name)
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('notes:detail', 'notes:edit', 'notes:delete'),
)
def test_pages_availability_for_author(author_client, name, note):
    """Автор может видеть, редактировать и удалять свою заметку."""
    url = reverse(name, args=(note.slug,))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lf('not_author_client'), HTTPStatus.NOT_FOUND),
        (lf('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('notes:detail', 'notes:edit', 'notes:delete'),
)
def test_pages_availability_for_different_users(
        parametrized_client, name, note, expected_status
):
    """Сравнение доступа к заметке для автора и постороннего."""
    url = reverse(name, args=(note.slug,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('notes:detail', lf('slug_for_args')),
        ('notes:edit', lf('slug_for_args')),
        ('notes:delete', lf('slug_for_args')),
        ('notes:add', None),
        ('notes:success', None),
        ('notes:list', None),
    ),
)
def test_redirects_for_anonymous_user(client, name, args):
    """Аноним должен перенаправляться на login с закрытых страниц."""
    login_url = reverse('users:login')
    url = reverse(name, args=args) if args else reverse(name)
    expected_url = f'{login_url}?next={url}'

    response = client.get(url)
    assertRedirects(response, expected_url)
