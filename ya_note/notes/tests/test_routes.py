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

    def test_home_page_available_for_anonymous(self):
        """Главная страница доступна анонимному пользователю."""
        url = reverse('notes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_available_for_authenticated_user(self):
        """Стр. списка, добавления и успеха доступны аутентиф. пользователю."""
        self.client.force_login(self.author)
        pages = ('notes:list', 'notes:add', 'notes:success')
        for name in pages:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_for_note_accessible_by_author(self):
        """Стр. заметки, редактирования и удаления доступны автору."""
        self.client.force_login(self.author)
        pages = ('notes:detail', 'notes:edit', 'notes:delete')
        for name in pages:
            with self.subTest(name=name):
                url = reverse(name, args=(self.note.slug,))
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_for_note_return_404_for_other_user(self):
        """Другой пользователь получает 404 при доступе к страницам заметки."""
        self.client.force_login(self.other_user)
        pages = ('notes:detail', 'notes:edit', 'notes:delete')
        for name in pages:
            with self.subTest(name=name):
                url = reverse(name, args=(self.note.slug,))
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_anonymous_redirected_to_login_for_protected_pages(self):
        """Аноним перенаправляется на логин при попытке доступа к защищ.стр."""
        pages = (
            'notes:list', 'notes:add', 'notes:success',
            'notes:detail', 'notes:edit', 'notes:delete'
        )
        for name in pages:
            with self.subTest(name=name):
                if name in ('notes:detail', 'notes:edit', 'notes:delete'):
                    url = reverse(name, args=(self.note.slug,))
                else:
                    url = reverse(name)
                response = self.client.get(url)
                expected_url = f'/auth/login/?next={url}'
                self.assertRedirects(response, expected_url)

    def test_auth_pages_available_for_all_users(self):
        """Стр. регистрации, входа и выхода доступны всем (в т.ч. анониму)."""
        url_login = reverse('users:login')
        url_signup = reverse('users:signup')
        response_login = self.client.get(url_login)
        response_signup = self.client.get(url_signup)
        self.assertEqual(response_login.status_code, HTTPStatus.OK)
        self.assertEqual(response_signup.status_code, HTTPStatus.OK)
        url_logout = reverse('users:logout')
        response_logout = self.client.post(url_logout)
        self.assertEqual(response_logout.status_code, HTTPStatus.FOUND)
