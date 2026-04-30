from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

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
    data = {'text': 'мой комментарий'}
    response = author_client.post(url, data)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(
        reverse('news:detail', args=(news.id,))
    )
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == 'мой комментарий'


@pytest.mark.django_db
def test_comment_with_bad_words_not_published(
    author_client, news, bad_words_data
):
    """Если комментарий содержит запрещённые слова, он не публикуется,
    а форма возвращает ошибку."""
    url = reverse('news:detail', args=(news.id,))
    for bad_word in bad_words_data:
        data = {'text': f'Плохое слово: {bad_word}'}
        response = author_client.post(url, data)
        form = response.context.get('form')
        assert form is not None
        assert 'text' in form.errors
        error_msg = 'Комментарий содержит запрещённые слова.'
        assert form.errors['text'][0] == error_msg
        assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_edit_own_comment(author_client, comment):
    """Авторизованный пользователь может редактировать свой комментарий."""
    edit_url = reverse('news:edit', args=(comment.id,))
    data = {'text': 'обновлённый текст'}
    response = author_client.post(edit_url, data)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(
        reverse('news:detail', args=(comment.news.id,))
    )
    comment.refresh_from_db()
    assert comment.text == 'обновлённый текст'


@pytest.mark.django_db
def test_author_can_delete_own_comment(author_client, comment):
    """Авторизованный пользователь может удалить свой комментарий."""
    delete_url = reverse('news:delete', args=(comment.id,))
    response = author_client.post(delete_url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(
        reverse('news:detail', args=(comment.news.id,))
    )
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_other_user_cannot_edit_others_comment(
    not_author_client, comment
):
    """Другой пользователь не может редактировать чужой комментарий."""
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
    """Другой пользователь не может удалить чужой комментарий."""
    delete_url = reverse('news:delete', args=(comment.id,))
    response = not_author_client.post(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
