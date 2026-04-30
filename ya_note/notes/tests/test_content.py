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
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.note = Note.objects.create(
            title='Test',
            text='Text',
            slug='test-slug',
            author=cls.user
        )

    def test_note_in_object_list(self):
        """Заметка автора есть в списке."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('notes:list'))
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_form_in_context(self):
        """Форма есть в контексте страницы создания."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('notes:add'))
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
