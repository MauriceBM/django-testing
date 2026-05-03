from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.tests.common import (
    create_test_note, create_test_user, get_logged_client
)

User = get_user_model()


class TestRoutes(TestCase):
    """Тесты маршрутов YaNote."""

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных."""
        cls.author = create_test_user('author')
        cls.other_user = create_test_user('other')
        cls.note = create_test_note(
            'Test', 'Text', 'test', cls.author
        )
        cls.author_client = get_logged_client(cls.author)
        cls.other_client = get_logged_client(cls.other_user)

    def test_home_page_available_for_anonymous(self):
        """Главная страница доступна анонимному пользователю."""
        url = reverse('notes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_available_for_authenticated_user(self):
        """Стр. списка, добавления и успеха доступны аутентиф. пользователю."""
        pages = ('notes:list', 'notes:add', 'notes:success')
        for name in pages:
            with self.subTest(page=name):
                url = reverse(name)
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_for_note_accessible_by_author(self):
        """Стр. заметки, редактирования и удаления доступны автору."""
        pages = ('notes:detail', 'notes:edit', 'notes:delete')
        for name in pages:
            with self.subTest(page=name):
                url = reverse(name, args=(self.note.slug,))
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_for_note_return_404_for_other_user(self):
        """Другой пользователь получает 404 при доступе к страницам заметки."""
        pages = ('notes:detail', 'notes:edit', 'notes:delete')
        for name in pages:
            with self.subTest(page=name):
                url = reverse(name, args=(self.note.slug,))
                response = self.other_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_anonymous_redirected_to_login_for_protected_pages(self):
        """Аноним перенаправляется на логин при доступе к защищённым стр."""
        pages = (
            'notes:list', 'notes:add', 'notes:success',
            'notes:detail', 'notes:edit', 'notes:delete'
        )
        login_path = '/auth/login/'
        for name in pages:
            with self.subTest(page=name):
                if name in ('notes:detail', 'notes:edit', 'notes:delete'):
                    url = reverse(name, args=(self.note.slug,))
                else:
                    url = reverse(name)
                response = self.client.get(url)
                expected_url = f"{login_path}?next={url}"
                self.assertRedirects(response, expected_url)

    def test_auth_pages_available_for_all_users(self):
        """Стр. регистрации, входа и выхода доступны всем."""
        login_url = reverse('users:login')
        signup_url = reverse('users:signup')
        logout_url = reverse('users:logout')

        response_login = self.client.get(login_url)
        response_signup = self.client.get(signup_url)
        response_logout = self.client.post(logout_url)

        self.assertEqual(response_login.status_code, HTTPStatus.OK)
        self.assertEqual(response_signup.status_code, HTTPStatus.OK)
        self.assertIn(
            response_logout.status_code, (HTTPStatus.OK, HTTPStatus.FOUND)
        )
