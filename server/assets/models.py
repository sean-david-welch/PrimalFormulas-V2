from django.db import models


# Create your models here.
class Assets(models.Model):
    id = models.UUIDField(primary_key=True)
    title = models.TextField()
    content = models.TextField()
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "assets"
