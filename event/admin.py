from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _

from event.models import Event, Recipient, RECIPIENT_SEX_CHOICE


class RecipientsInLine(admin.TabularInline):
    model = Recipient
    fk_name = 'event'
    fields = ('name', 'surname', 'distance', 'email')
    extra = 1


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', )


class EventListFilter(admin.SimpleListFilter):
    title = _('Мероприятие')
    parameter_name = 'Мероприятие'

    def lookups(self, request, model_admin):
        events = Event.objects.all().order_by('-id')
        return tuple([(event.id, event.name) for event in events])

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        return queryset.filter(event_id=self.value())


class SexListFilter(admin.SimpleListFilter):
    title = _('Пол')
    parameter_name = 'Пол'

    def lookups(self, request, model_admin):
        return RECIPIENT_SEX_CHOICE

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        return queryset.filter(sex=self.value())


class CountryListFilter(admin.SimpleListFilter):
    title = _('Страна')
    parameter_name = 'Страна'

    def lookups(self, request, model_admin):
        countries = []
        country_list = []
        recipients = Recipient.objects.all()

        for recipient in recipients:
            if recipient.country not in country_list:
                country_list.append(recipient.country)
                countries.append((recipient.country, recipient.country))

        return tuple(countries)

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        return queryset.filter(country=self.value())


class RecipientAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'birth_date', 'country', 'phone', 'email')

    search_fields = ('name', 'surname')
    list_filter = (EventListFilter, SexListFilter, CountryListFilter)


admin.site.unregister(Group)
admin.site.unregister(User)
