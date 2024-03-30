import uuid
from django.db import models


# Create your models here.
class Assets(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField()
    content = models.TextField()
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = True
        db_table = "assets"
