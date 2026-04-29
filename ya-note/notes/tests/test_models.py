from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from django.contrib.auth.models import User
from notes.models import Note


class NoteModelTests(TestCase):
    """Тесты модели заметки YaNote."""

    @classmethod
    def setUpTestData(cls):
        """Создание пользователя для тестов."""
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_str_method(self):
        """Проверка строкового представления заметки."""
        note = Note.objects.create(
            title='Тестовая заметка',
            text='Содержимое',
            slug='test',
            author=self.user
        )
        self.assertEqual(str(note), 'Тестовая заметка')

    def test_slug_auto_generation(self):
        """Проверка автогенерации slug при пустом значении."""
        note = Note(
            title='Вторая заметка',
            text='Описание',
            slug='',
            author=self.user
        )
        note.save()
        self.assertEqual(note.slug, 'vtoraya-zametka')

    def test_slug_uniqueness_constraint(self):
        """Проверка уникальности slug на уровне БД."""
        Note.objects.create(
            title='Первая',
            text='Текст',
            slug='unique-slug',
            author=self.user
        )
        duplicate = Note(
            title='Вторая',
            text='Текст',
            slug='unique-slug',
            author=self.user
        )
        with self.assertRaises(IntegrityError):
            duplicate.save()

    def test_required_fields_validation(self):
        """Проверка валидации обязательных полей."""
        note = Note(
            title='',
            text='',
            slug='empty-fields',
            author=self.user
        )
        with self.assertRaises(ValidationError):
            note.full_clean()
