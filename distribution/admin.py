from django.contrib import admin

from distribution.forms import DistributionCreateForm
from material.admin.options import MaterialModelAdmin
from material.admin.decorators import register
from django.utils.translation import gettext_lazy as _

from distribution.models import Distribution, DistributionItem


class DistributionItemInLine(admin.StackedInline):
    model = DistributionItem
    fk_name = 'distribution'
    readonly_fields = ('recipient', 'is_sent')
    fields = ('recipient', 'is_sent')
    extra = 0
    can_delete = False


@register(Distribution)
class DistributionAdmin(MaterialModelAdmin):
    list_display = ('name', 'send_date', 'is_sent')
    form = DistributionCreateForm
    icon_name = 'mail'


class EventListFilter(admin.SimpleListFilter):
    title = _('Рассылка')
    parameter_name = 'Рассылка'

    def lookups(self, request, model_admin):
        distribution = Distribution.objects.all()
        return tuple([(event.id, event.name) for event in distribution])

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        return queryset.filter(distribution_id=self.value())


@register(DistributionItem)
class DistributionItemAdmin(MaterialModelAdmin):
    list_display = ('recipient', 'is_sent')
    list_filter = (EventListFilter, 'is_sent')
    icon_name = 'playlist_add_check'
