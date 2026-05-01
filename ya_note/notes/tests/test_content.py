from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from notes.tests.common import (
    create_test_note, create_test_user, get_logged_client
)

User = get_user_model()


class TestContent(TestCase):
    """Тесты контента YaNote."""

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных."""
        cls.author = create_test_user('author')
        cls.other_user = create_test_user('other')
        cls.note = create_test_note(
            'Test', 'Text', 'test', cls.author
        )
        cls.other_note = create_test_note(
            'Other', 'Other text', 'other', cls.other_user
        )
        cls.author_client = get_logged_client(cls.author)

    def test_note_in_list_for_author(self):
        """Отдельная заметка передаётся на страницу списка."""
        response = self.author_client.get(reverse('notes:list'))
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_other_user_notes_not_in_list(self):
        """В список заметок одного пользователя не попадают заметки другого."""
        response = self.author_client.get(reverse('notes:list'))
        object_list = response.context['object_list']
        self.assertNotIn(self.other_note, object_list)

    def test_form_on_create_page(self):
        """На страницу создания заметки передаётся форма."""
        response = self.author_client.get(reverse('notes:add'))
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_form_on_edit_page(self):
        """На страницу редактирования заметки передаётся форма."""
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.author_client.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
