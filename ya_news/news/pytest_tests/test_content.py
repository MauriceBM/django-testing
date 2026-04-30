import pytest
from django.conf import settings
from django.urls import reverse
from news.models import News


@pytest.mark.django_db
def test_news_count_on_home(client):
    """На главной не более настроечного количества новостей."""
    response = client.get(reverse('news:home'))
    news_list = response.context['object_list']
    assert news_list.count() <= settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_sorted_by_date(client):
    """Новости отсортированы от новых к старым."""
    response = client.get(reverse('news:home'))
    news_list = response.context['object_list']
    dates = [n.date for n in news_list]
    assert dates == sorted(dates, reverse=True)
