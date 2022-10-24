from django.shortcuts import render
from django.views.generic import View

from news.models import Article


# Create your views here.


class IndexView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        slider_articles = articles[:5]
        square_articles = articles[:10]
        breaking_news = articles.filter(status="BREAKING")[:5]
        trending_articles = articles.filter(trending=True)
        latest_articles = articles[:13]

        context = {'slider_articles': slider_articles, 'square_articles': square_articles,
                   'breaking_news': breaking_news, 'trending_articles': trending_articles,
                   'latest_articles': latest_articles, 'articles': articles}
        return render(request, 'news/main.html', context)
