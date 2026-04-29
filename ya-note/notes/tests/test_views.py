from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


class NoteRouteTests(TestCase):
    """Тесты маршрутов проекта YaNote."""

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных один раз для всех тестов."""
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.note = Note.objects.create(
            title='Первая заметка',
            text='Текст первой заметки.',
            slug='first-note',
            author=cls.user
        )

    def setUp(self):
        """Авторизация пользователя перед каждым тестом."""
        self.client.login(
            username='testuser',
            password='testpass123'
        )

    def test_notes_list_status_200(self):
        """Проверка статуса 200 на странице списка заметок."""
        url = reverse('notes:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Первая заметка')

    def test_note_detail_valid_slug(self):
        """Проверка страницы заметки с валидным slug."""
        url = reverse(
            'notes:detail',
            kwargs={'slug': self.note.slug}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.note.title)
        self.assertContains(response, self.note.text)

    def test_note_detail_invalid_slug_404(self):
        """Проверка страницы заметки с несуществующим slug."""
        url = reverse(
            'notes:detail',
            kwargs={'slug': 'no-slug-here'}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_note_form_get(self):
        """Проверка отображения формы создания заметки."""
        url = reverse('notes:add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_note_post_empty_slug(self):
        """Проверка автогенерации slug при создании заметки."""
        url = reverse('notes:add')
        form_data = {
            'title': 'Вторая заметка',
            'text': 'Текст второй заметки.',
            'slug': ''
        }
        response = self.client.post(url, data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Note.objects.filter(title='Вторая заметка').exists()
        )

    def test_create_note_post_duplicate_slug(self):
        """Проверка ошибки валидации при дублировании slug."""
        url = reverse('notes:add')
        form_data = {
            'title': 'Дубликат',
            'text': 'Текст дубликата.',
            'slug': self.note.slug
        }
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 200)
        # Сообщение об ошибке содержит значение slug, используем точный текст
        self.assertFormError(
            response.context['form'],
            'slug',
            'first-note - такой slug уже существует,'
            ' придумайте уникальное значение!'
        )
