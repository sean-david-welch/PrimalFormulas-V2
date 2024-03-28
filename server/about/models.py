from django.db import models


# Create your models here.
class About(models.Model):
    id = models.UUIDField(primary_key=True)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "about"
