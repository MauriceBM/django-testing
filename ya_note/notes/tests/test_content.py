from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestNoteListPage(TestCase):
    """Тестирование страницы со списком заметок."""

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных."""
        cls.author = User.objects.create(username='АвторЗаметки')
        cls.other_user = User.objects.create(username='ДругойПользователь')
        cls.note = Note.objects.create(
            title='Тестовая заметка',
            text='Текст заметки',
            slug='test-slug',
            author=cls.author,
        )

    def test_note_in_list_for_author(self):
        """Заметка автора отображается в списке для него."""
        self.client.force_login(self.author)
        response = self.client.get(reverse('notes:list'))
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_note_not_in_list_for_other_user(self):
        """Заметка не отображается в списке для другого пользователя."""
        self.client.force_login(self.other_user)
        response = self.client.get(reverse('notes:list'))
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)


class TestNoteCreateEditPage(TestCase):
    """Тестирование страниц создания и редактирования заметки."""

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных."""
        cls.author = User.objects.create(username='АвторФормы')
        cls.note = Note.objects.create(
            title='Заметка для редактирования',
            text='Старый текст',
            slug='edit-slug',
            author=cls.author,
        )

    def test_create_page_contains_form(self):
        """На странице создания заметки передаётся форма."""
        self.client.force_login(self.author)
        response = self.client.get(reverse('notes:add'))
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_edit_page_contains_form(self):
        """На странице редактирования заметки передаётся форма."""
        self.client.force_login(self.author)
        response = self.client.get(
            reverse('notes:edit', args=(self.note.slug,))
        )
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
