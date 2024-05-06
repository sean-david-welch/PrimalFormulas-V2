import uuid
from django.db import models


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.TextField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.TextField(max_length=200, default="default.jpg")
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:  # type: ignore
        managed = True
        ordering = ["created"]
        db_table = "products"

    def __str__(self) -> str:
        return self.name
