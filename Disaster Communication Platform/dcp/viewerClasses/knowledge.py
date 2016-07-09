from dcp.customForms.goodsFroms import *
from dcp.viewerClasses.timeline import TimelineView
from dcp.viewerClasses.authentication import getPageAuthenticated
from dcp.views import View, LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from dcp.customForms.pollsForms import *
from dcp.models.catastrophe import *
from dcp.models.profile import *
from dcp.models.polls import Choice, Question

class Wissen(LoginRequiredMixin,View):
    template = 'dcp/content/wissen/wissen.html'

    def get(self, request):
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template)

class PollsView(LoginRequiredMixin,View):
	
	
	def get(self, request):
		latest_question_list = Question.objects.all()
		questionform = QuestionForm()

		for question in latest_question_list:
			if question.choice_text:
				if question.choice_text[len(question.choice_text) - 1] == ";":
					question.choice_text = question.choice_text[:len(question.choice_text) - 2]
				all_choices = question.choice_text.split(";")

				
				for c in all_choices:
					if c[0] == " ":
						c = c[1:]
					if (not (Choice.objects.filter(text = c, question = question).exists())):
						choice = Choice(text=c,
							votes=0,
							question=question)
						choice.save()


		choice_list = Choice.objects.all()

		context = {'latest_question_list': latest_question_list, 'choice_list': choice_list, 'questionform' : questionform}
		template = 'dcp/content/wissen/polls.html'
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

	def post(self, request):
		template = 'dcp/content/wissen/polls.html'
		post_identifier = request.POST.get('post_identifier')
		if post_identifier == 'create' and request.user.is_active and request.user.is_authenticated():
			questionform = QuestionForm(request.POST)
			if questionform.is_valid():
				question = Question(title=request.POST.get('title'), 
					text=request.POST.get('text'), 
					pub_date=timezone.now(),
					user=request.user,
					catastrophe=Catastrophe.objects.get(id=request.POST.get('catastrophe')),
					choice_text=request.POST.get('choice_text'))
				question.save()
		elif post_identifier == 'vote' and request.user.is_active and request.user.is_authenticated():
			selected_choice = Choice.objects.get(id = request.POST.get('choice'))
			selected_choice.votes += 1
			voted_question = selected_choice.question
			voted_question.voted_users.add(request.user)
			selected_choice.save()
		return HttpResponseRedirect("/wissen/")
