"""
Database models.
"""

from django.conf import settings
from django.db import models

# Create your models here.


class Recipe(models.Model):
    """Recipe Object"""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
