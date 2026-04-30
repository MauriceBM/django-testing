from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    """Тесты маршрутов YaNote."""

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

    def test_list_page_status(self):
        """Страница списка возвращает 200."""
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_detail_page_status(self):
        """Страница заметки возвращает 200 для автора."""
        self.client.force_login(self.user)
        url = reverse('notes:detail', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
