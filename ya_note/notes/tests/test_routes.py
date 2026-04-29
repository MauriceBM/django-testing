from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    """Тестирование маршрутов проекта YaNote."""

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных для проверки маршрутов."""
        cls.author = User.objects.create(
            username='АвторЗаметки'
        )
        cls.other_user = User.objects.create(
            username='ДругойПользователь'
        )
        cls.note = Note.objects.create(
            title='Тестовая заметка',
            text='Текст заметки',
            slug='test-slug',
            author=cls.author,
        )

    def test_anonymous_client_has_access_to_home(self):
        """Главная страница доступна анонимному пользователю."""
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_anonymous_client_has_access_to_auth_pages(self):
        """Страницы регистрации и входа доступны анонимному пользователю."""
        auth_pages = (
            'users:login',
            'users:signup',
            'users:logout',
        )
        for name in auth_pages:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK
                )

    def test_anonymous_client_is_redirected_to_login(self):
        """Аноним перенаправляется на страницу логина."""
        restricted_urls = (
            reverse('notes:add'),
            reverse('notes:edit', args=(self.note.slug,)),
            reverse('notes:delete', args=(self.note.slug,)),
        )
        login_url = reverse('users:login')

        for url in restricted_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.FOUND
                )
                expected = f'{login_url}?next={url}'
                self.assertRedirects(response, expected)

    def test_author_has_access_to_detail_page(self):
        """Автор имеет доступ к странице своей заметки."""
        self.client.force_login(self.author)
        url = reverse('notes:detail', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_other_user_has_no_access_to_detail_page(self):
        """Другой пользователь не имеет доступа к чужой заметке."""
        self.client.force_login(self.other_user)
        url = reverse('notes:detail', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_other_user_has_no_access_to_edit_page(self):
        """Другой пользователь не может редактировать чужую заметку."""
        self.client.force_login(self.other_user)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_other_user_has_no_access_to_delete_page(self):
        """Другой пользователь не может удалить чужую заметку."""
        self.client.force_login(self.other_user)
        url = reverse('notes:delete', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
