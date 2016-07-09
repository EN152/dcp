from .imports import *
from .catastrophe import *
from .profile import *

import dcp.dcpSettings


class Question(models.Model):
	title = models.CharField(max_length=200)
	text = models.TextField(max_length=500, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)
	catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=True)
	choice_text = models.CharField(max_length=500, null=False, default="Ja; Nein")
	pub_date = models.DateTimeField('date published', default=timezone.now())

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
	text = models.CharField(max_length=200, null=True)
	votes = models.IntegerField(default=0)
	#user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)
	question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, blank=True)

	def __str__(self):
		return self.choice_text