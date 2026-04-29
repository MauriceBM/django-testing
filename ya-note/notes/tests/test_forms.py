from django.test import TestCase

from django.contrib.auth.models import User
from notes.models import Note
from notes.forms import NoteForm


class NoteFormTests(TestCase):
    """Тесты формы создания и редактирования заметок."""

    @classmethod
    def setUpTestData(cls):
        """Подготовка пользователя и существующей заметки."""
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.existing = Note.objects.create(
            title='Существующая',
            text='Текст',
            slug='existing',
            author=cls.user
        )

    def test_valid_form_submission(self):
        """Проверка валидных данных формы."""
        form_data = {
            'title': 'Новая запись',
            'text': 'Содержимое заметки',
            'slug': 'new-record'
        }
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_title_validation(self):
        """Проверка ошибки при пустом заголовке."""
        form_data = {
            'title': '',
            'text': 'Текст',
            'slug': 'no-title'
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_duplicate_slug_validation(self):
        """Проверка ошибки при дублировании slug."""
        form_data = {
            'title': 'Дубль',
            'text': 'Текст',
            'slug': 'existing'
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('slug', form.errors)

    def test_form_preserves_manual_slug(self):
        """Проверка сохранения вручную указанного slug."""
        form_data = {
            'title': 'Ручной slug',
            'text': 'Текст',
            'slug': 'custom-slug'
        }
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['slug'], 'custom-slug')
