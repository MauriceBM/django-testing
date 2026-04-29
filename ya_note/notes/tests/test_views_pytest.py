import pytest
from django.urls import reverse
from pytest_django.asserts import (
    assertContains,
    assertRedirects,
    assertFormError,
)

from notes.models import Note


@pytest.mark.django_db
class TestNoteViews:
    """Тесты маршрутов проекта YaNote в стиле pytest."""

    def test_notes_list_status_200(self, admin_client, admin_user):
        """Проверка статуса 200 на странице списка заметок."""
        Note.objects.create(
            title='Первая заметка',
            text='Текст первой заметки.',
            slug='first-note',
            author=admin_user
        )
        url = reverse('notes:list')
        response = admin_client.get(url)
        assert response.status_code == 200
        assertContains(response, 'Первая заметка')

    def test_note_detail_valid_slug(self, admin_client, admin_user):
        """Проверка страницы заметки с валидным slug."""
        note = Note.objects.create(
            title='Первая заметка',
            text='Текст первой заметки.',
            slug='first-note',
            author=admin_user
        )
        url = reverse(
            'notes:detail',
            kwargs={'slug': note.slug}
        )
        response = admin_client.get(url)
        assert response.status_code == 200
        assertContains(response, note.title)
        assertContains(response, note.text)

    def test_note_detail_invalid_slug_404(self, admin_client):
        """Проверка страницы заметки с несуществующим slug."""
        url = reverse(
            'notes:detail',
            kwargs={'slug': 'no-slug-here'}
        )
        response = admin_client.get(url)
        assert response.status_code == 404

    def test_create_note_form_get(self, admin_client):
        """Проверка отображения формы создания заметки."""
        url = reverse('notes:add')
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_create_note_post_empty_slug(self, admin_client, admin_user):
        """Проверка автогенерации slug при создании заметки."""
        url = reverse('notes:add')
        form_data = {
            'title': 'Вторая заметка',
            'text': 'Текст второй заметки.',
            'slug': ''
        }
        response = admin_client.post(url, data=form_data, follow=True)
        assert response.status_code == 200
        assert Note.objects.filter(
            title='Вторая заметка',
            author=admin_user
        ).exists()

    def test_create_note_post_duplicate_slug(self, admin_client, admin_user):
        """Проверка ошибки валидации при дублировании slug."""
        existing = Note.objects.create(
            title='Первая',
            text='Текст',
            slug='uniq-slug',
            author=admin_user
        )
        url = reverse('notes:add')
        form_data = {
            'title': 'Дубликат',
            'text': 'Текст дубликата.',
            'slug': existing.slug
        }
        response = admin_client.post(url, data=form_data)
        assert response.status_code == 200
        assert 'такой slug уже существует' in response.content.decode('utf-8')

    def test_anonymous_user_redirected_to_login(self, client):
        """Проверка, что аноним перенаправляется на логин."""
        url = reverse('notes:list')
        response = client.get(url)
        assertRedirects(
            response,
            f'/auth/login/?next={url}'
        )
