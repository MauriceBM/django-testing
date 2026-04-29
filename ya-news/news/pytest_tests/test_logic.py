import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from news.models import Comment


@pytest.mark.django_db
def test_anonymous_cant_comment(client, news, form_data):
    """Анонимный пользователь не может отправить комментарий."""
    url = reverse('news:detail', args=(news.id,))
    response = client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_comment(author_client, news, form_data):
    """Авторизованный пользователь может отправить комментарий."""
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=form_data)

    assert response.status_code == HTTPStatus.FOUND
    assert str(news.id) in response.url
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_bad_words_blocked(author_client, news, form_data):
    """Комментарий с запрещёнными словами не публикуется."""
    original_count = Comment.objects.count()

    form_data['text'] = 'запрещённое_слово'
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=form_data)

    assert Comment.objects.count() == original_count

    if response.context and response.context.get('form'):
        form = response.context['form']
        if hasattr(form, 'errors') and form.errors:
            assert 'text' in form.errors
    else:
        assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
def test_author_can_edit_comment(author_client, comment, form_data):
    """Автор может редактировать свой комментарий."""
    url = reverse('news:edit', args=(comment.id,))
    response = author_client.post(url, data=form_data)

    assert response.status_code == HTTPStatus.FOUND

    assert str(comment.news.id) in response.url
    comment.refresh_from_db()
    assert comment.text.lower() == form_data['text'].lower()


@pytest.mark.django_db
def test_other_user_cant_edit_comment(not_author_client, comment, form_data):
    """Другой пользователь не может редактировать чужой комментарий."""
    url = reverse('news:edit', args=(comment.id,))
    response = not_author_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text != form_data['text']
