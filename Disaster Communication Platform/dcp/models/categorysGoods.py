from django.db import models
from django.utils import timezone
import datetime

class CategorysGoods(models.Model):
    """description of class"""
    name = models.CharField(max_length=200, null=False, unique=True, primary_key=True)
    glyphiconString = models.CharField(max_length=200, null=False)
    created_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name