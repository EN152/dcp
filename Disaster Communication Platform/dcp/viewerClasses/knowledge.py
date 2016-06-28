from dcp.customForms.goodsFroms import *
from dcp.viewerClasses.timeline import TimelineView
from dcp.viewerClasses.authentication import getPageAuthenticated
from dcp.views import View, LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from dcp.customForms.pollsForms import *

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
        form = QuestionForm()
        template = 'dcp/content/wissen/polls.html'
        context = {'latest_question_list': latest_question_list, 'form' : form}

        return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)