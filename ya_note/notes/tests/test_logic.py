from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.tests.common import (
    SLUG_ERROR_MSG, create_test_note, create_test_user, get_logged_client
)

User = get_user_model()


class TestLogic(TestCase):
    """Тесты логики YaNote."""

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных."""
        cls.author = create_test_user('author')
        cls.other_user = create_test_user('other')
        cls.note = create_test_note(
            'Test', 'Text', 'test', cls.author
        )
        cls.author_client = get_logged_client(cls.author)
        cls.other_client = get_logged_client(cls.other_user)

    def test_authenticated_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку."""
        url = reverse('notes:add')
        data = {'title': 'New', 'text': 'New text', 'slug': 'new'}
        response = self.author_client.post(url, data)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 2)

    def test_anonymous_user_cannot_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        url = reverse('notes:add')
        data = {'title': 'New', 'text': 'New text', 'slug': 'new'}
        response = self.client.post(url, data)
        login_url = f"{reverse('users:login')}?next={url}"
        self.assertRedirects(response, login_url)
        self.assertEqual(Note.objects.count(), 1)

    def test_cannot_create_two_notes_with_same_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        url = reverse('notes:add')
        data = {
            'title': 'Duplicate', 'text': 'Text', 'slug': self.note.slug
        }
        response = self.author_client.post(url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        form = response.context['form']
        self.assertIn('slug', form.errors)
        self.assertEqual(form.errors['slug'][0], SLUG_ERROR_MSG)
        self.assertEqual(Note.objects.count(), 1)

    def test_slug_auto_generated_if_empty(self):
        """Если slug не заполнен, формируется автоматически через pytils."""
        url = reverse('notes:add')
        data = {'title': 'Авто slug', 'text': 'Text', 'slug': ''}
        response = self.author_client.post(url, data)
        self.assertRedirects(response, reverse('notes:success'))
        new_note = Note.objects.get(title='Авто slug')
        self.assertTrue(new_note.slug)

    def test_author_can_edit_note(self):
        """Пользователь peut редак-ть свою заметку."""
        url = reverse('notes:edit', args=(self.note.slug,))
        data = {'title': 'Edited', 'text': 'Edited text', 'slug': 'edited'}
        response = self.author_client.post(url, data)
        self.assertRedirects(response, reverse('notes:success'))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Edited')

    def test_other_user_cannot_edit_other_note(self):
        """Пользователь ne peut pas редак-ть чужую заметку."""
        url = reverse('notes:edit', args=(self.note.slug,))
        data = {'title': 'Hack', 'text': 'Hack text', 'slug': 'hack'}
        response = self.other_client.post(url, data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertNotEqual(self.note.title, 'Hack')

    def test_author_can_delete_note(self):
        """Пользователь может удалить свою заметку."""
        url = reverse('notes:delete', args=(self.note.slug,))
        response = self.author_client.post(url)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 0)

    def test_other_user_cannot_delete_other_note(self):
        """Пользователь ne peut pas удалить чужую заметку."""
        url = reverse('notes:delete', args=(self.note.slug,))
        response = self.other_client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)
