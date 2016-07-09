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

class PostNewsView(TimelineView):
	def get(self, request, form=None):
		if form is None:
			form = PostNewsForm
		return super().getCreateNew(request, 'glyphicon-info-sign', 'btn-warning' , 'Wissen: Neuigkeiten' , form, 'Post_News')

	def post(self, request):
		if request.POST.get('post_identifier') == 'create' and request.user.is_active and request.user.is_authenticated():
			form = PostNewsForm(request.POST, request.FILES)
			if form.is_valid():
				return super().createNewGood(request, form)
			return self.get(request, form)
		return super().post(request)

class PostDangersView(TimelineView):
	def get(self, request, form=None):
		if form is None:
			form = PostDangersForm
		return super().getCreateNew(request, 'glyphicon-info-sign', 'btn-warning' , 'Wissen: Gefahren' , form, 'Post_Dangers')

	def post(self, request):
		if request.POST.get('post_identifier') == 'create' and request.user.is_active and request.user.is_authenticated():
			form = PostDangersForm(request.POST, request.FILES)
			if form.is_valid():
				return super().createNewGood(request, form)
			return self.get(request, form)
		return super().post(request)

class PostQuestionsView(TimelineView):
	def get(self, request, form=None):
		if form is None:
			form = PostQuestionsForm
		return super().getCreateNew(request, 'glyphicon-info-sign', 'btn-warning' , 'Wissen: Fragen' , form, 'Post_Questions')

	def post(self, request):
		if request.POST.get('post_identifier') == 'create' and request.user.is_active and request.user.is_authenticated():
			form = PostQuestionsForm(request.POST, request.FILES)
			if form.is_valid():
				return super().createNewGood(request, form)
			return self.get(request, form)
		return super().post(request)

	
class PollsView(LoginRequiredMixin,View):
	
	
	def get(self, request):
		latest_question_list = Question.objects.all()
		questionform = QuestionForm()

		for question in latest_question_list:
			if question.choice_text:
				all_choices = question.choice_text.split(";")
				
				for c in all_choices:
					if not Choice.objects.filter(text = c, question = question).exists():
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
			selected_choice = Choice.objects.filter(id = request.POST.get('choice'))[0]
			selected_choice.votes += 1
		return HttpResponseRedirect("/wissen/abstimmungen/")
			