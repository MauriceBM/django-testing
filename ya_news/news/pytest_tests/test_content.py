import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
def test_news_limit(client):
    response = client.get(reverse('news:home'))
    news_list = response.context['object_list']
    assert news_list.count() <= settings.NEWS_COUNT_ON_HOME_PAGE
