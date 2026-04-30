from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestLogic(TestCase):
    """Тесты логики прав доступа YaNote."""

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username='author',
            password='testpass123'
        )
        cls.other = User.objects.create_user(
            username='other',
            password='testpass123'
        )
        cls.note = Note.objects.create(
            title='Test',
            text='Text',
            slug='test-slug',
            author=cls.author
        )

    def test_author_can_edit_own_note(self):
        """Автор может открыть страницу редактирования."""
        self.client.force_login(self.author)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_other_cannot_edit_foreign_note(self):
        """Другой пользователь получает 404 при редактировании."""
        self.client.force_login(self.other)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
