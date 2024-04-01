import uuid
from django.db import models


# Create your models here.
class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(max_length=200)
    content = models.TextField(default="default.jpg")
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = True
        ordering = ["created"]
        db_table = "assets"

    def __str__(self):
        return self.title
