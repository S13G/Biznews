from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

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
    admin = models.ForeignKey(User, related_name='articles', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    text = RichTextField(config_name="awesome_ckeditor", null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    trending = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    image = models.ImageField(null=True, upload_to='news/articles')
    views = models.IntegerField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.title)

    @property
    def image_url(self):
        try:
            url = self.image.url
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