from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestLogic(TestCase):
    """Тесты логики YaNote."""

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных."""
        cls.author = User.objects.create_user(
            username='author', password='pass123'
        )
        cls.other_user = User.objects.create_user(
            username='other', password='pass123'
        )
        cls.note = Note.objects.create(
            title='Test', text='Text', slug='test', author=cls.author
        )

    def test_authenticated_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку."""
        self.client.force_login(self.author)
        url = reverse('notes:add')
        data = {'title': 'New', 'text': 'New text', 'slug': 'new'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 2)

    def test_anonymous_user_cannot_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        url = reverse('notes:add')
        data = {'title': 'New', 'text': 'New text', 'slug': 'new'}
        response = self.client.post(url, data)
        login_url = reverse('users:login') + f'?next={url}'
        self.assertRedirects(response, login_url)
        self.assertEqual(Note.objects.count(), 1)

    def test_cannot_create_two_notes_with_same_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        self.client.force_login(self.author)
        url = reverse('notes:add')
        data = {'title': 'Duplicate', 'text': 'Text', 'slug': self.note.slug}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(
            response.context['form'], 'slug',
            'Заметка с таким slug уже существует'
        )
        self.assertEqual(Note.objects.count(), 1)

    def test_slug_auto_generated_if_empty(self):
        """Если slug не заполнен, формируется автоматически через pytils."""
        self.client.force_login(self.author)
        url = reverse('notes:add')
        data = {'title': 'Авто slug', 'text': 'Text', 'slug': ''}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('notes:success'))
        new_note = Note.objects.get(title='Авто slug')
        self.assertTrue(new_note.slug)

    def test_author_can_edit_note(self):
        """Пользователь может редактировать свою заметку."""
        self.client.force_login(self.author)
        url = reverse('notes:edit', args=(self.note.slug,))
        data = {'title': 'Edited', 'text': 'Edited text', 'slug': 'edited'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('notes:success'))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Edited')

    def test_other_user_cannot_edit_note(self):
        """Пользователь не может редактировать чужую заметку."""
        self.client.force_login(self.other_user)
        url = reverse('notes:edit', args=(self.note.slug,))
        data = {'title': 'Hack', 'text': 'Hack text', 'slug': 'hack'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertNotEqual(self.note.title, 'Hack')

    def test_author_can_delete_note(self):
        """Пользователь может удалить свою заметку."""
        self.client.force_login(self.author)
        url = reverse('notes:delete', args=(self.note.slug,))
        response = self.client.post(url)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 0)

    def test_other_user_cannot_delete_note(self):
        """Пользователь не может удалить чужую заметку."""
        self.client.force_login(self.other_user)
        url = reverse('notes:delete', args=(self.note.slug,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)
