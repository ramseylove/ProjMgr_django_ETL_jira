from django.contrib.auth.models import AbstractUser
from django.db import models

from project_tracking.models import Project 


class CustomUser(AbstractUser):
    projects = models.ManyToManyField(Project)

    def __str__(self):
        return self.email
