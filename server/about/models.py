import uuid
from django.db import models


class About(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.TextField(default="default.jpg")
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = True
        ordering = ["created"]
        db_table = "about"

    def __str__(self) -> str:
        return self.title
