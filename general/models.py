from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


# Create your models here.


class SiteDetail(models.Model):
    name = models.CharField(max_length=200, default='BIZNEWS', null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    twitter = models.URLField(null=True)
    linkedin = models.URLField(null=True)
    facebook = models.URLField(null=True)
    instagram = models.URLField(null=True)
    youtube = models.URLField(null=True)

    def save(self, *args, **kwargs):
        if not self.pk and SiteDetail.objects.exists():
            raise ValidationError('There can be only one site detail instance')
        return super(SiteDetail, self).save(*args, **kwargs)


class Subscriber(models.Model):
    email = models.EmailField(null=True)
    exported = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.email)


class Contact(models.Model):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    subject = models.CharField(max_length=255, null=True)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)