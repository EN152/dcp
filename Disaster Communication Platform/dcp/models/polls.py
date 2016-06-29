from .imports import *
from .catastrophe import *
from .profile import *

import dcp.dcpSettings

#CHOICES_TEXT = ('Ja', 'Nein')

class Choice(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)
	catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=False)
	#choice_text = models.CharField(max_length=200)#, choices=CHOICES_TEXT)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text

class Question(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)
	#catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=False)
	question_text = models.CharField(max_length=200)
	#pub_date = models.DateTimeField('date published')
	description = models.TextField(max_length=500, null=True, blank=True)
    #image = forms.ImageField(required=False, label='Foto (optional)')
   	#location_x = forms.FloatField(required=True, initial=0, widget=forms.HiddenInput())
    #location_y = forms.FloatField(required=True, initial=0, widget=forms.HiddenInput())	
	#choice = models.ManyToManyField(Choice)
	choice_text = models.CharField(max_length=200, default=2)#, choices=CHOICES_TEXT)
	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

