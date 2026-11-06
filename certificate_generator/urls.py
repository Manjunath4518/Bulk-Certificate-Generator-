from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from generator import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("generate/", views.generate_certificates, name="generate"),
    path("download/<str:batch_id>/", views.download_batch, name="download_batch"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
