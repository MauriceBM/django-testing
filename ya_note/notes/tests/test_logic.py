from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestLogic(TestCase):
    """Тесты логики YaNote."""

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author')
        cls.other = User.objects.create(username='other')
        cls.note = Note.objects.create(
            title='Test',
            text='Text',
            slug='test',
            author=cls.author
        )

    def test_author_can_edit(self):
        """Автор может редактировать свою заметку."""
        self.client.force_login(self.author)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_other_cannot_edit(self):
        """Другой пользователь не может редактировать чужую заметку."""
        self.client.force_login(self.other)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
