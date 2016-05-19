from __future__ import unicode_literals

from django.db import models

class Catastrophe(models.Model):
	cat_title = models.CharField(max_length=200)
	cat_location = models.CharField(max_length=100)
	cat_pub_date = models.DateTimeField('date published')

    	def __unicode__(self):
			return self.cat_title