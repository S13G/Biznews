import sweetify
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from general.forms import SubscriberForm
from news.forms import CommentForm, ReplyForm
from news.models import Article, Category, Comment


# Create your views here.


# function to call all objects from the database to be passed to the templates
class IndexView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all().select_related('category')
        slider_articles = articles[:5]
        square_articles = articles[:4]
        breaking_news = articles.filter(status="BREAKING")[:5]
        trending_articles = articles.filter(status="TRENDING")
        latest_articles = articles[:13]
        featured_articles = articles.filter(featured=True)[:15]
        categories = Category.objects.all()
        newsletter_form = SubscriberForm()

        context = {'slider_articles': slider_articles, 'square_articles': square_articles,
                   'breaking_news': breaking_news, 'trending_articles': trending_articles,
                   'latest_articles': latest_articles, 'articles': articles, 'featured_articles': featured_articles,
                   'categories': categories, 'newsletter_form': newsletter_form}
        return render(request, 'news/main.html', context)

    def post(self, request, *args, **kwargs):
        newsletter_form = SubscriberForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            sweetify.success(request, title="Subscribed!", text="Your subscription was successful", button="ok",
                             timer=3500, icon="success")
            return redirect('/')
        else:
            sweetify.error(request, title="Something went wrong",
                           text="Please make sure you enter a correct email try again later", button="ok",
                           timer=3500, icon="error")
            return redirect('/')


# for displaying the details of each article
class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all().select_related('category')
        trending_articles = articles.filter(status="TRENDING")[:5]
        try:
            article = Article.objects.get(slug=self.kwargs.get('article_slug'))
        except Article.DoesNotExist:
            raise Http404()

        comment_form = CommentForm()
        newsletter_form = SubscriberForm()
        reply_form = ReplyForm()

        context = {'article': article, 'trending_articles': trending_articles, 'comment_form': comment_form,
                   'reply_form': reply_form, 'newsletter_form': newsletter_form}
        return render(request, 'news/article-detail.html', context)

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        reply_form = ReplyForm(request.POST)
        newsletter_form = SubscriberForm(request.POST)

        if 'article_slug' in request.POST:
            if comment_form.is_valid():
                instance = comment_form.save(commit=False)
                instance.article = Article.objects.get(slug=request.POST.get('article_slug'))
                instance.save()
                return JsonResponse({'name': instance.name, 'email': instance.email, 'website': instance.website,
                                     'message': instance.message})
            else:
                return JsonResponse({'error': 'Comment not submitted'})
        elif 'comment_id' in request.POST:
            if reply_form.is_valid():
                instance = reply_form.save(commit=False)
                instance.comment = Comment.objects.get(id=request.POST.get('comment_id'))
                instance.save()
                return JsonResponse({'error': 'Comment not submitted'})
        else:
            if newsletter_form.is_valid():
                newsletter_form.save()
                sweetify.success(request, title="Subscribed!", text="Your subscription was successful", button="ok",
                                 timer=3500, icon="success")
                return redirect(f"articles/{self.kwargs.get('article_slug')}")
            else:
                sweetify.error(request, title="Something went wrong",
                               text="Please make sure you enter a correct email try again later", button="ok",
                               timer=3500, icon="error")
                return redirect(f"articles/{self.kwargs.get('article_slug')}")

