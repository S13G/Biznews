from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from import_export import resources
from import_export.admin import ExportActionMixin
from .models import Subscriber, SiteDetail, Contact


# Register your models here.


@admin.register(SiteDetail)
class SiteDetailAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {
            'fields': (
                'name', 'email', 'phone', 'address'
            ),
        }),
        ('Social', {
            'fields': (
                'twitter', 'facebook', 'linkedin', 'instagram', 'youtube'
            ),
        }),
    )

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        if self.model.objects.all().count() == 1:
            obj = self.model.objects.all()[0]
            return HttpResponseRedirect(
                reverse("admin:%s_%s_change" % (self.model._meta.app_label, self.model._meta.model_name),
                        args=(obj.id,)))
        return super(SiteDetailAdmin, self).changelist_view(request=request, extra_context=extra_context)


class SubscriberResource(resources.ModelResource):
    class Meta:
        model = Subscriber
        fields = ['email']

    def after_export(self, queryset, data, *args, **kwargs):
        queryset.update(exported=True)
        return queryset


@admin.register(Subscriber)
class SubscriberAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['email', 'exported', 'timestamp']
    list_filter = ['email', 'exported', 'timestamp']
    resource_class = SubscriberResource

    fieldsets = (
        ('General', {
            'fields': (
                'email', 'exported', 'timestamp'
            ),
        }),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'timestamp']
    list_filter = ['name', 'email', 'subject', 'timestamp']

    fieldsets = (
        ('General', {
            'fields': (
                'name', 'email', 'subject', 'timestamp'
            ),
        }),
    )
