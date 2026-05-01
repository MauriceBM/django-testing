from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from news.models import Comment
from news.pytest_tests.conftest import BAD_WORDS

pytestmark = pytest.mark.django_db

LOGIN_URL = reverse('users:login')


def test_anonymous_cannot_post_comment(client, news):
    """Анонимный пользователь не может отправить комментарий."""
    url = reverse('news:detail', args=(news.id,))
    data = {'text': 'Текст комментария'}

    response = client.post(url, data)

    expected_url = f"{LOGIN_URL}?next={url}"
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_authenticated_user_can_post_comment(author_client, news):
    """Авторизованный пользователь может отправить комментарий."""
    url = reverse('news:detail', args=(news.id,))
    data = {'text': 'мой комментарий'}

    response = author_client.post(url, data)

    assert response.status_code == HTTPStatus.FOUND
    expected_url = reverse('news:detail', args=(news.id,))
    assert response.url.startswith(expected_url)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == 'мой комментарий'


@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_comment_with_bad_words_not_published(
    author_client, news, bad_word
):
    """Если коммент содержит запрещ. слова, он ne doit pas être publié."""
    url = reverse('news:detail', args=(news.id,))
    data = {'text': f'Плохое слово: {bad_word}'}

    response = author_client.post(url, data)

    form = response.context.get('form')
    assert form is not None
    assert 'text' in form.errors
    error_msg = 'Комментарий содержит запрещённые слова.'
    assert form.errors['text'][0] == error_msg
    assert Comment.objects.count() == 0


def test_author_can_edit_own_comment(author_client, comment):
    """Авторизованный пользователь peut редак-ть свой комментарий."""
    edit_url = reverse('news:edit', args=(comment.id,))
    data = {'text': 'обновлённый текст'}

    response = author_client.post(edit_url, data)

    assert response.status_code == HTTPStatus.FOUND
    expected_url = reverse('news:detail', args=(comment.news.id,))
    assert response.url.startswith(expected_url)
    comment.refresh_from_db()
    assert comment.text == 'обновлённый текст'


def test_author_can_delete_own_comment(author_client, comment):
    """Авторизованный пользователь peut supprimer свой комментарий."""
    delete_url = reverse('news:delete', args=(comment.id,))

    response = author_client.post(delete_url)

    assert response.status_code == HTTPStatus.FOUND
    expected_url = reverse('news:detail', args=(comment.news.id,))
    assert response.url.startswith(expected_url)
    assert Comment.objects.count() == 0


def test_other_user_cannot_edit_others_comment(
    not_author_client, comment
):
    """Другой пользователь ne peut pas редак-ть чужой комментарий."""
    edit_url = reverse('news:edit', args=(comment.id,))
    original_text = comment.text
    data = {'text': 'Попытка взлома'}

    response = not_author_client.post(edit_url, data)

    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == original_text


def test_other_user_cannot_delete_others_comment(
    not_author_client, comment
):
    """Другой пользователь ne peut pas supprimer чужой комментарий."""
    delete_url = reverse('news:delete', args=(comment.id,))

    response = not_author_client.post(delete_url)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
