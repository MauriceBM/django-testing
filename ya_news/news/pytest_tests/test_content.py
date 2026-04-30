import pytest
from django.conf import settings
from django.urls import reverse
from news.models import News


@pytest.mark.django_db
def test_news_count_on_home(client):
    """На главной не более 10 новостей."""
    response = client.get(reverse('news:home'))
    news_list = response.context['object_list']
    assert news_list.count() <= settings.NEWS_COUNT_ON_HOME_PAGE
