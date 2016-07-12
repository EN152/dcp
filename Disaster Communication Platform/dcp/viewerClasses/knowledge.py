from numpy.core.tests.test_numerictypes import read_values_nested

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
from dcp.models.knowledge import *

class Wissen(LoginRequiredMixin,View):
    template = 'dcp/content/wissen/wissen.html'

    def get(self, request):
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template)

class Neuigkeiten(LoginRequiredMixin,View):
    template = 'dcp/content/wissen/neuigkeiten.html'

    def post(self,request):
        if "search_submit" in request.POST:
            try:
                KnowledgeSearchResultList = KnowledgeNews.objects.all().filter(title__contains=request.POST['search'])
                KnowledgeSearchResultList = KnowledgeSearchResultList.order_by('-created_date')
                for forEachKnowledgeSearchResult in KnowledgeSearchResultList:
                    forEachKnowledgeSearchResult.description = forEachKnowledgeSearchResult.description[0:200]
                knowledgeYourList = KnowledgeNews.objects.all().filter(userID=request.user.id).order_by('-created_date')
                for forEachknowledge in knowledgeYourList:
                    forEachknowledge.description = forEachknowledge.description[0:200]

                context ={
                    'knowledgeYourList': knowledgeYourList,
                    'knowledgeList': KnowledgeSearchResultList
                }
            except KnowledgeNews.DoesNotExist or Exception:
                KnowledgeSearchResultList = None
                knowledgeYourList = None
                context = None
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template,context)

    def get(self, request):
        if (request.user is None):
            return dcp.viewerClasses.authentication.getPageAuthenticated(request, RegisterView.template,context)
        try:
            knowledgeYourList = KnowledgeNews.objects.all().filter(userID=request.user.id).order_by('-created_date')
            for forEachknowledge in knowledgeYourList:
                forEachknowledge.description = forEachknowledge.description[0:200]
            knowledgeList = KnowledgeNews.objects.all().order_by('-created_date')
            for forEachknowledge in knowledgeList:
                forEachknowledge.description = forEachknowledge.description[0:200]
            context ={
                'knowledgeYourList': knowledgeYourList,
                'knowledgeList': knowledgeList
            }
        except KnowledgeNews.DoesNotExist or Exception:
            knowledgeYourList = None
            knowledgeList = None
            context = None

        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template,context)

class NeuigkeitenBearbeiten(LoginRequiredMixin,View):
    template = 'dcp/content/wissen/neuigkeitenBearbeiten.html'

    def get(self, request):
        return HttpResponseRedirect("../")

    def post(self,request):
        if "delete" in request.POST:
            try:
                knowledgeID = request.POST['knowledgeID']
                knowledgeEntity = KnowledgeNews.objects.get(id=knowledgeID)
                knowledgeEntity.delete()
                return HttpResponseRedirect("../")
            except KnowledgeNews.DoesNotExist or Exception:
                return HttpResponseRedirect("../")
        if "send" in request.POST:
            try:
                knowledgeID = request.POST['knowledgeID']
                knowledgeEntity = KnowledgeNews.objects.get(id=knowledgeID)
                knowledgeEntity.description = request.POST['description']
                knowledgeEntity.title = request.POST['title']
                knowledgeEntity.created_date = timezone.now()
                knowledgeEntity.save()
            except KnowledgeNews.DoesNotExist or Exception:
                return HttpResponseRedirect("../")
            return HttpResponseRedirect("../")
        try:
            knowledgeID = request.POST['knowledgeID']
            knowledgeEntity = KnowledgeNews.objects.get(id=knowledgeID)
        except KnowledgeNews.DoesNotExist:
            return HttpResponseRedirect("../")
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template,{"knowledgeEntity":knowledgeEntity})

class NeuigkeitenAnsehen(LoginRequiredMixin,View):
    template = 'dcp/content/wissen/neuigkeitenAnsehen.html'

    def get(self, request):
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template)

    def post(self,request):
        try:
            knowledgeID = request.POST['knowledgeID']
            knowledgeEntity = KnowledgeNews.objects.get(id=knowledgeID)
            knowledgeUser = User.objects.get(id=knowledgeEntity.userID)
            context ={
                "knowledgeEntity":knowledgeEntity,
                "knowledgeUser":knowledgeUser
            }

        except KnowledgeNews.DoesNotExist or Exception:
            return HttpResponseRedirect("../")

        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template,context)

class NeuigkeitenAnlegen(LoginRequiredMixin,View):
    template = 'dcp/content/wissen/neuigkeitenAnlegen.html'

    def get(self, request):
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template)

    def post(self,request):
        if "send" in request.POST:
            try:
                knowledgeEntity = KnowledgeNews.objects.create(title=request.POST['title'],description=request.POST['description'],userID=request.user.id)
                knowledgeEntity.save()
            except KnowledgeNews.DoesNotExist or Exception:
                return HttpResponseRedirect("../")
            return HttpResponseRedirect("../")
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template)


class PollsView(LoginRequiredMixin,View):
	
	
	def get(self, request):
		latest_question_list = Question.objects.all()
		questionform = QuestionForm()

		for question in latest_question_list:
			if question.choice_text:
				if question.choice_text[len(question.choice_text) - 1] == ";":
					question.choice_text = question.choice_text[:len(question.choice_text) - 1]
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

		elif post_identifier == 'delete' and request.user.is_active and request.user.is_authenticated():
			question_id = request.POST.get('question_id')
			choice_set = Choice.objects.filter(question = question_id)
			choice_set.delete()
			del_question = Question.objects.get(id = question_id)
			del_question.delete()

		return HttpResponseRedirect("/wissen/abstimmungen/")
