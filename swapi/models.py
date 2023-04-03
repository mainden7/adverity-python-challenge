import os

from django.conf import settings
from django.db import models


class FilesCollection(models.Model):
    file = models.FileField(upload_to=settings.FILES_BASE_DIR)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        return os.path.basename(self.file.name)
