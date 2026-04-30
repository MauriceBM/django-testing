from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError

from news.models import Comment


@pytest.mark.django_db
def test_anonymous_cannot_post_comment(client, news):
    """Анонимный пользователь не может отправить комментарий."""
    url = reverse('news:detail', args=(news.id,))
    data = {'text': 'Текст комментария'}
    response = client.post(url, data)
    login_url = reverse('users:login') + f'?next={url}'
    assertRedirects(response, login_url)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_authenticated_user_can_post_comment(author_client, news):
    """Авторизованный пользователь может отправить комментарий."""
    url = reverse('news:detail', args=(news.id,))
    data = {'text': 'Мой комментарий'}
    response = author_client.post(url, data)
    assertRedirects(response, url)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == 'Мой комментарий'
    assert comment.author == author_client._user
    assert comment.news == news


@pytest.mark.django_db
def test_comment_with_bad_words_not_published(
    author_client, news, bad_words_data
):
    url = reverse('news:detail', args=(news.id,))
    for bad_word in bad_words_data:
        data = {'text': f'Плохое слово: {bad_word}'}
        response = author_client.post(url, data)
        assertFormError(
            response,
            'form',
            'text',
            'Обнаружено запрещённое слово'
        )
        assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_edit_own_comment(author_client, comment):
    """Авторизованный пользователь может редактировать свой коммент."""
    edit_url = reverse('news:edit', args=(comment.id,))
    data = {'text': 'Обновлённый текст'}
    response = author_client.post(edit_url, data)
    assertRedirects(
        response,
        reverse('news:detail', args=(comment.news.id,))
    )
    comment.refresh_from_db()
    assert comment.text == 'Обновлённый текст'


@pytest.mark.django_db
def test_author_can_delete_own_comment(author_client, comment):
    """Авторизованный пользователь может удалить свой коммент."""
    delete_url = reverse('news:delete', args=(comment.id,))
    response = author_client.post(delete_url)
    assertRedirects(
        response,
        reverse('news:detail', args=(comment.news.id,))
    )
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_other_user_cannot_edit_others_comment(
    not_author_client, comment
):
    """Авториз. пользователь не может редактировать чужой коммент."""
    edit_url = reverse('news:edit', args=(comment.id,))
    data = {'text': 'Попытка взлома'}
    response = not_author_client.post(edit_url, data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text != 'Попытка взлома'


@pytest.mark.django_db
def test_other_user_cannot_delete_others_comment(
    not_author_client, comment
):
    """Авториз. пользователь не может удалить чужой коммент."""
    delete_url = reverse('news:delete', args=(comment.id,))
    response = not_author_client.post(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
