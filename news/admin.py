from django.contrib import admin

from .models import Category, Article, Comment, Reply


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'timestamp']
    list_filter = ['name']

    fieldsets = (
        ('General', {
            'fields': (
                'name', 'timestamp'
            ),
        }),
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['admin', 'title', 'category', 'trending', 'timestamp']
    list_filter = ['admin', 'title', 'category', 'trending', 'timestamp']
    readonly_fields = ['admin']

    fieldsets = (
        ('General', {
            'fields': (
                'admin', 'title', 'text', 'category', 'image'
            ),
        }),
        ('Checks', {
            'fields': (
                'trending', 'timestamp'
            ),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.admin = request.user
        obj.save()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'name', 'email', 'website']
    list_filter = ['article', 'name', 'email', 'website']

    fieldsets = (
        ('General', {
            'fields': (
                'article', 'name', 'email', 'website', 'message', 'timestamp'
            ),
        }),
    )


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['comment', 'name', 'email']
    list_filter = ['comment', 'name', 'email']

    fieldsets = (
        ('General', {
            'fields': (
                'comment', 'name', 'email', 'message', 'timestamp'
            ),
        }),
    )