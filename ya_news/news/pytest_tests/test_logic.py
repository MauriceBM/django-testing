from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from news.models import Comment
from news.pytest_tests.conftest import BAD_WORDS
from news.pytest_tests.urls import LOGIN_URL, DETAIL_URL_NAME

pytestmark = pytest.mark.django_db

COMMENT_TEXT = 'Текст комментария'
EDITED_TEXT = 'обновлённый текст'
HACK_TEXT = 'Попытка взлома'
BAD_WORD_ERROR = 'Комментарий содержит запрещённые слова.'


def test_anonymous_cannot_post_comment(client, news):
    """Анонимный пользователь не может отправить комментарий."""
    url = reverse(DETAIL_URL_NAME, args=(news.id,))
    data = {'text': COMMENT_TEXT}
    initial_count = Comment.objects.count()

    response = client.post(url, data)

    expected_url = f"{LOGIN_URL}?next={url}"
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == initial_count


def test_authenticated_user_can_post_comment(author_client, news):
    """Авторизованный пользователь может отправить комментарий."""
    url = reverse(DETAIL_URL_NAME, args=(news.id,))
    data = {'text': 'мой комментарий'}
    initial_count = Comment.objects.count()

    response = author_client.post(url, data)

    assert response.status_code == HTTPStatus.FOUND
    expected_url = reverse(DETAIL_URL_NAME, args=(news.id,))
    assert response.url.startswith(expected_url)
    assert Comment.objects.count() == initial_count + 1
    comment = Comment.objects.get()
    assert comment.text == 'мой комментарий'


@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_comment_with_bad_words_not_published(
    author_client, news, bad_word
):
    """Комментарий с запрещёнными словами не публикуется."""
    url = reverse(DETAIL_URL_NAME, args=(news.id,))
    data = {'text': f'Плохое слово: {bad_word}'}
    initial_count = Comment.objects.count()

    response = author_client.post(url, data)

    form = response.context.get('form')
    assert form is not None
    assert 'text' in form.errors
    assert form.errors['text'][0] == BAD_WORD_ERROR
    assert Comment.objects.count() == initial_count


def test_author_can_edit_own_comment(author_client, comment):
    """Автор может редактировать свой комментарий."""
    edit_url = reverse('news:edit', args=(comment.id,))
    data = {'text': EDITED_TEXT}

    response = author_client.post(edit_url, data)

    assert response.status_code == HTTPStatus.FOUND
    expected_url = reverse(DETAIL_URL_NAME, args=(comment.news.id,))
    assert response.url.startswith(expected_url)
    comment.refresh_from_db()
    assert comment.text == EDITED_TEXT


def test_other_user_cannot_edit_others_comment(
    not_author_client, comment
):
    """Другой пользователь не может редактировать чужой комментарий."""
    edit_url = reverse('news:edit', args=(comment.id,))
    original_text = comment.text
    data = {'text': HACK_TEXT}

    response = not_author_client.post(edit_url, data)

    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == original_text


def test_author_can_delete_own_comment(author_client, comment):
    """Автор может удалить свой комментарий."""
    delete_url = reverse('news:delete', args=(comment.id,))
    initial_count = Comment.objects.count()

    response = author_client.post(delete_url)

    assert response.status_code == HTTPStatus.FOUND
    expected_url = reverse(DETAIL_URL_NAME, args=(comment.news.id,))
    assert response.url.startswith(expected_url)
    assert Comment.objects.count() == initial_count - 1


def test_other_user_cannot_delete_others_comment(
    not_author_client, comment
):
    """Другой пользователь не может удалить чужой комментарий."""
    delete_url = reverse('news:delete', args=(comment.id,))
    initial_count = Comment.objects.count()

    response = not_author_client.post(delete_url)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == initial_count
