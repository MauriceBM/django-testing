"""Тесты маршрутов YaNote."""
from http import HTTPStatus

from django.urls import reverse

from notes.tests.common import BaseTest

LOGIN_PATH = '/auth/login/'

PAGES_WITHOUT_ARGS = (
    'notes:list',
    'notes:add',
    'notes:success',
)

PAGES_WITH_NOTE_ARG = (
    'notes:detail',
    'notes:edit',
    'notes:delete',
)

AUTH_GET_PAGES = (
    'users:login',
    'users:signup',
)


class TestRoutes(BaseTest):
    """Тесты маршрутов YaNote."""

    def test_pages_availability(self):
        """Проверка доступности страниц для разных пользователей."""
        test_cases = (
            # Client, URL Name, Args, Expected Status
            (self.client, 'notes:home', None, HTTPStatus.OK),
            (self.author_client, 'notes:list', None, HTTPStatus.OK),
            (self.author_client, 'notes:add', None, HTTPStatus.OK),
            (self.author_client, 'notes:success', None, HTTPStatus.OK),
            (
                self.author_client,
                'notes:detail',
                (self.note.slug,),
                HTTPStatus.OK,
            ),
            (
                self.author_client,
                'notes:edit',
                (self.note.slug,),
                HTTPStatus.OK,
            ),
            (
                self.author_client,
                'notes:delete',
                (self.note.slug,),
                HTTPStatus.OK,
            ),
            (
                self.other_client,
                'notes:detail',
                (self.note.slug,),
                HTTPStatus.NOT_FOUND,
            ),
            (
                self.other_client,
                'notes:edit',
                (self.note.slug,),
                HTTPStatus.NOT_FOUND,
            ),
            (
                self.other_client,
                'notes:delete',
                (self.note.slug,),
                HTTPStatus.NOT_FOUND,
            ),
            (self.client, 'users:login', None, HTTPStatus.OK),
            (self.client, 'users:signup', None, HTTPStatus.OK),
        )

        for client, name, args, expected_status in test_cases:
            with self.subTest(
                client=client,
                page=name,
                status=expected_status,
            ):
                url = reverse(name, args=args)
                response = client.get(url)
                self.assertEqual(
                    response.status_code, expected_status
                )

    def test_redirects_for_anonymous_user(self):
        """Анонимный пользователь перенаправляется на страницу входа."""
        test_cases = (
            *[(name, None) for name in PAGES_WITHOUT_ARGS],
            *[
                (name, (self.note.slug,))
                for name in PAGES_WITH_NOTE_ARG
            ],
        )

        for name, args in test_cases:
            with self.subTest(page=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                expected_url = f'{LOGIN_PATH}?next={url}'
                self.assertRedirects(response, expected_url)

    def test_logout_page_available_for_all_users(self):
        """Страница выхода доступна всем."""
        url = reverse('users:logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
