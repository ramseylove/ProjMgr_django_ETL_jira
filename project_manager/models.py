from django.db import models

from django_extensions.db.fields import AutoSlugField

class Project(models.Model):
    url = models.URLField()
    p_key = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='p_key')
    p_id = models.IntegerField()

    def __str__(self):
        return self.name
