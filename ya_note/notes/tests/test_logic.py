from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestLogic(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='author', password='pass123')
        cls.other = User.objects.create_user(username='other', password='pass123')
        cls.note = Note.objects.create(title='Test', text='Text', slug='test', author=cls.author)

    def test_author_can_edit(self):
        self.client.force_login(self.author)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_other_cannot_edit(self):
        self.client.force_login(self.other)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
