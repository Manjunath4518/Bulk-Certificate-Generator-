import uuid
from django.db import models

class CertificateBatch(models.Model):
    batch_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    template = models.ImageField(upload_to="templates/")
    csv_file = models.FileField(upload_to="csv/")
    created_at = models.DateTimeField(auto_now_add=True)
    certificate_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Batch {self.batch_id}"
