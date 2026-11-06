from django.contrib import admin
from .models import CertificateBatch

@admin.register(CertificateBatch)
class CertificateBatchAdmin(admin.ModelAdmin):
    list_display = ("batch_id", "certificate_count", "created_at")
    readonly_fields = ("batch_id", "created_at", "certificate_count")
