from django.urls import reverse

from notes.forms import NoteForm
from notes.tests.common import BaseTest

FORM_CONTEXT_KEY = 'form'


class TestContent(BaseTest):
    """Тесты контента YaNote."""

    def test_note_in_list_for_author(self):
        """Отдельная заметка передаётся на страницу списка."""
        response = self.author_client.get(reverse('notes:list'))
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_other_user_notes_not_in_list(self):
        """Заметки другого пользователя не попадают в список."""
        response = self.author_client.get(reverse('notes:list'))
        object_list = response.context['object_list']
        self.assertNotIn(self.other_note, object_list)

    def test_form_on_create_page(self):
        """На страницу создания заметки передаётся форма."""
        response = self.author_client.get(reverse('notes:add'))
        self.assertIn(FORM_CONTEXT_KEY, response.context)
        self.assertIsInstance(
            response.context[FORM_CONTEXT_KEY], NoteForm
        )

    def test_form_on_edit_page(self):
        """На страницу редактирования заметки передаётся форма."""
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.author_client.get(url)
        self.assertIn(FORM_CONTEXT_KEY, response.context)
        self.assertIsInstance(
            response.context[FORM_CONTEXT_KEY], NoteForm
        )
