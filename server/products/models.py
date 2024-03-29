from django.db import models


class Products(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
