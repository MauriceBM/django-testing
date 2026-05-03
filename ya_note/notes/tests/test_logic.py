from http import HTTPStatus

from django.urls import reverse

from notes.models import Note
from notes.tests.common import SLUG_ERROR_MSG, BaseTest

ADD_URL = reverse('notes:add')
SUCCESS_URL = reverse('notes:success')
LOGIN_URL_NAME = 'users:login'

NEW_NOTE_DATA = {'title': 'New', 'text': 'New text', 'slug': 'new'}
EDITED_NOTE_DATA = {
    'title': 'Edited', 'text': 'Edited text', 'slug': 'edited'
}
HACK_NOTE_DATA = {
    'title': 'Hack', 'text': 'Hack text', 'slug': 'hack'
}
AUTO_SLUG_DATA = {'title': 'Авто slug', 'text': 'Text', 'slug': ''}
DUPLICATE_SLUG_DATA = {
    'title': 'Duplicate', 'text': 'Text', 'slug': 'test'
}


class TestLogic(BaseTest):
    """Тесты логики YaNote."""

    def test_authenticated_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку."""
        initial_count = Note.objects.count()
        response = self.author_client.post(ADD_URL, NEW_NOTE_DATA)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), initial_count + 1)

    def test_anonymous_user_cannot_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        initial_count = Note.objects.count()
        response = self.client.post(ADD_URL, NEW_NOTE_DATA)
        login_url = f"{reverse(LOGIN_URL_NAME)}?next={ADD_URL}"
        self.assertRedirects(response, login_url)
        self.assertEqual(Note.objects.count(), initial_count)

    def test_cannot_create_two_notes_with_same_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        initial_count = Note.objects.count()
        response = self.author_client.post(
            ADD_URL, DUPLICATE_SLUG_DATA
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        form = response.context['form']
        self.assertIn('slug', form.errors)
        self.assertEqual(form.errors['slug'][0], SLUG_ERROR_MSG)
        self.assertEqual(Note.objects.count(), initial_count)

    def test_slug_auto_generated_if_empty(self):
        """Если slug пустой, генерация через pytils."""
        response = self.author_client.post(ADD_URL, AUTO_SLUG_DATA)
        self.assertRedirects(response, SUCCESS_URL)
        new_note = Note.objects.get(title='Авто slug')
        self.assertTrue(new_note.slug)

    def test_author_can_edit_note(self):
        """Автор может редактировать свою заметку."""
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.author_client.post(url, EDITED_NOTE_DATA)
        self.assertRedirects(response, SUCCESS_URL)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Edited')

    def test_other_user_cannot_edit_other_note(self):
        """Другой пользователь не может редактировать чужую заметку."""
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.other_client.post(url, HACK_NOTE_DATA)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertNotEqual(self.note.title, 'Hack')

    def test_author_can_delete_note(self):
        """Автор может удалить свою заметку."""
        initial_count = Note.objects.count()
        url = reverse('notes:delete', args=(self.note.slug,))
        response = self.author_client.post(url)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), initial_count - 1)

    def test_other_user_cannot_delete_other_note(self):
        """Другой пользователь не может удалить чужую заметку."""
        initial_count = Note.objects.count()
        url = reverse('notes:delete', args=(self.note.slug,))
        response = self.other_client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), initial_count)
