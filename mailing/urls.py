from django.urls import path, include
from django.conf.urls.static import static

from mailing import settings


urlpatterns = [
    path('api/event/', include('event.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('material.admin.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
