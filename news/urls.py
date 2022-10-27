from django.urls import path

from news import views

app_name = 'news'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('articles/<slug:article_slug>/', views.ArticleDetailView.as_view(), name='article-detail')
]
