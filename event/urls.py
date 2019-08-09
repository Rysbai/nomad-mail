from django.urls import path

from event import views

name = "event"
urlpatterns = [
    path('get_all', views.get_events, name="get_events"),
    path('get_recipients', views.get_recipients, name="get_recipients"),
    path('get_all_distances', views.get_all_distances, name="get_all_distances"),
    path('get_recipients_by_ids', views.get_recipients_by_ids, name='get_recipients_by_ids'),
    path('get_all_participants_country', views.get_all_participants_country, name="get_all_participants_country")
]
