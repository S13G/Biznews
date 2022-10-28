from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=25, null=True)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Categories'


class Article(models.Model):
    NEWS_STATUS = (
        ('BREAKING', 'BREAKING'),
        ('TRENDING', 'TRENDING'),
    )
    admin = models.ForeignKey(User, related_name='articles', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    text = RichTextField(config_name="awesome_ckeditor", null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    featured = models.BooleanField(default=False)
    status = models.CharField(choices=NEWS_STATUS, max_length=255, null=True, blank=True)
    image = models.ImageField(null=True, upload_to='news/articles')
    views = models.IntegerField(default="0", null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'article_slug': self.slug})

    @property
    def imageURL(self):
        try:
            url = self.image.url # set this image
        except:
            url = ''  # set default image
        return url


class ArticleView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='articles')
    ip = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.ip)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(null=True, max_length=100)
    email = models.EmailField(null=True)
    website = models.URLField(null=True, blank=True)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    name = models.CharField(null=True, max_length=100)
    email = models.EmailField(null=True)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Replies'
