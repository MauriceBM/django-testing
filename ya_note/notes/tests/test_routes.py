from http import HTTPStatus

from django.urls import reverse

from notes.tests.common import BaseTest

LOGIN_PATH = '/auth/login/'
PAGES_WITHOUT_ARGS = ('notes:list', 'notes:add', 'notes:success')
PAGES_WITH_NOTE_ARG = ('notes:detail', 'notes:edit', 'notes:delete')
ALL_PROTECTED_PAGES = PAGES_WITHOUT_ARGS + PAGES_WITH_NOTE_ARG
AUTH_GET_PAGES = ('users:login', 'users:signup')


class TestRoutes(BaseTest):
    """Тесты маршрутов YaNote."""

    def test_home_page_available_for_anonymous(self):
        """Главная страница доступна анонимному пользователю."""
        url = reverse('notes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_available_for_authenticated_user(self):
        """Страницы списка, добавления и успеха доступны авторизованному."""
        for name in PAGES_WITHOUT_ARGS:
            with self.subTest(page=name):
                url = reverse(name)
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_for_note_accessible_by_author(self):
        """Страницы заметки, редактирования и удаления доступны автору."""
        for name in PAGES_WITH_NOTE_ARG:
            with self.subTest(page=name):
                url = reverse(name, args=(self.note.slug,))
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_for_note_return_404_for_other_user(self):
        """Другой пользователь получает 404 при доступе к страницам заметки."""
        for name in PAGES_WITH_NOTE_ARG:
            with self.subTest(page=name):
                url = reverse(name, args=(self.note.slug,))
                response = self.other_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_anonymous_redirected_to_login_for_protected_pages(self):
        """Аноним перенаправляется на логин при доступе."""
        for name in ALL_PROTECTED_PAGES:
            with self.subTest(page=name):
                if name in PAGES_WITH_NOTE_ARG:
                    url = reverse(name, args=(self.note.slug,))
                else:
                    url = reverse(name)
                response = self.client.get(url)
                expected_url = f"{LOGIN_PATH}?next={url}"
                self.assertRedirects(response, expected_url)

    def test_auth_pages_get_available_for_all_users(self):
        """Страницы регистрации и входа доступны всем (GET)."""
        for name in AUTH_GET_PAGES:
            with self.subTest(page=name, method='GET'):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_logout_page_available_for_all_users(self):
        """Страница выхода доступна всем (POST)."""
        url = reverse('users:logout')
        response = self.client.post(url)
        self.assertIn(
            response.status_code, (HTTPStatus.OK, HTTPStatus.FOUND)
        )
