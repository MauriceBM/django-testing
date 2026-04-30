from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):
    """Тесты контента YaNote."""

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
        cls.other_note = Note.objects.create(
            title='Other', text='Other text', slug='other',
            author=cls.other_user
        )

    def test_note_in_list_for_author(self):
        """Отд. заметка передаётся на страницу списка в object_list."""
        self.client.force_login(self.author)
        response = self.client.get(reverse('notes:list'))
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_other_user_notes_not_in_list(self):
        """В список заметок одного пользователя не попадают заметки другого."""
        self.client.force_login(self.author)
        response = self.client.get(reverse('notes:list'))
        object_list = response.context['object_list']
        self.assertNotIn(self.other_note, object_list)

    def test_form_on_create_page(self):
        """На страницу создания заметки передаётся форма."""
        self.client.force_login(self.author)
        response = self.client.get(reverse('notes:add'))
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_form_on_edit_page(self):
        """На страницу редактирования заметки передаётся форма."""
        self.client.force_login(self.author)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
