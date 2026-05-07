from django.urls import reverse

HOME_URL = reverse('news:home')

LOGIN_URL = reverse('users:login')
SIGNUP_URL = reverse('users:signup')
LOGOUT_URL = reverse('users:logout')

DETAIL_URL_NAME = 'news:detail'
EDIT_URL_NAME = 'news:edit'
DELETE_URL_NAME = 'news:delete'
