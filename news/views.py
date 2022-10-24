from django.shortcuts import render
from django.views.generic import View

from news.models import Article, Category


# Create your views here.


class IndexView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        slider_articles = articles[:5]
        square_articles = articles[:4]
        breaking_news = articles.filter(status="BREAKING")[:5]
        trending_articles = articles.filter(status="TRENDING")
        latest_articles = articles[:13]
        featured_articles = articles.filter(featured=True)[:15]
        categories = Category.objects.all()

        context = {'slider_articles': slider_articles, 'square_articles': square_articles,
                   'breaking_news': breaking_news, 'trending_articles': trending_articles,
                   'latest_articles': latest_articles, 'articles': articles, 'featured_articles': featured_articles,
                   'categories': categories}
        return render(request, 'news/main.html', context)
