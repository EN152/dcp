from dcp.customForms.goodsFroms import *
from dcp.viewerClasses.timeline import TimelineView
from dcp.viewerClasses.authentication import getPageAuthenticated
from dcp.views import View, LoginRequiredMixin
from dcp.models.polls import Choice, Question
from django.views import generic

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

class PollsView(generic.ListView):
    template_name = 'dcp/content/wissen/polls.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')