# Generated by Django 4.1.2 on 2022-10-26 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_remove_article_trending_article_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterField(
            model_name='article',
            name='views',
            field=models.IntegerField(default='0', null=True),
        ),
    ]
