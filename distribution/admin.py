from django.contrib import admin

from distribution.forms import DistributionCreateForm
from django.utils.translation import gettext_lazy as _

from distribution.models import Distribution, DistributionItem


class DistributionItemInLine(admin.StackedInline):
    model = DistributionItem
    fk_name = 'distribution'
    readonly_fields = ('recipient', 'is_sent')
    fields = ('recipient', 'is_sent')
    extra = 0
    can_delete = False


class DistributionAdmin(admin.ModelAdmin):
    list_display = ('name', 'send_date', 'is_sent')
    fieldsets = (
        (None, {
            'fields': ('name', 'subject', 'body', 'send_date')
        }),
        ("Выбор получателей", {
            'fields': ('for_event', 'to_sex', 'to_countries')
        })
    )


class DistributionListFilter(admin.SimpleListFilter):
    title = _('Рассылка')
    parameter_name = 'Рассылка'

    def lookups(self, request, model_admin):
        distribution = Distribution.objects.all().order_by('-id')
        return tuple([(event.id, event.name) for event in distribution])

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        return queryset.filter(distribution_id=self.value())


class DistributionItemAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'is_sent')
    list_filter = (DistributionListFilter, 'is_sent')


admin.site.register(Distribution, DistributionAdmin)
admin.site.register(DistributionItem, DistributionItemAdmin)
admin.site.site_header = _("Nomad Sport Mail")
admin.site.site_title = _("Nomad Sport Mail")
