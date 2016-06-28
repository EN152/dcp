from .imports import *
from .catastrophe import *
from .profile import *

import dcp.dcpSettings

class Question(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)
	catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=False)
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)
	catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=False)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text