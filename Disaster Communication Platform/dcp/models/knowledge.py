from .imports import *
from dcp.customclasses import Helpers



class KnowledgeNews(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=15000)
    created_date = models.DateTimeField(default=timezone.now)
    userID = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)])
    bumpCounter = models.IntegerField(default=0)



    def __unicode__(self):  # def __str__(self):
        return self.title

