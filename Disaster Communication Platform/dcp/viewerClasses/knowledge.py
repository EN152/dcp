from dcp.customForms.knowledgeFroms import *
from dcp.viewerClasses.timeline import TimelineView
from dcp.viewerClasses.authentication import getPageAuthenticated
from dcp.views import View, LoginRequiredMixin

class Wissen(View):
    template = 'dcp/content/wissen/wissen.html'

    def get(self, request):
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template)

class PostNewsView(TimelineView):
    def get(self, request, form=None):
        if form is None:
            form = PostNewsForm
        return super().getCreateNew(request, 'glyphicon-info-sign', 'btn-yellow' , 'Wissen: Neuigkeiten' , form, None, 'Post_News')

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
        return super().getCreateNew(request, 'glyphicon-info-sign', 'btn-yellow' , 'Wissen: Gefahren' , form, None, 'Post_Dangers')

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
        return super().getCreateNew(request, 'glyphicon-info-sign', 'btn-yellow' , 'Wissen: Fragen' , form, None, 'Post_Questions')

    def post(self, request):
        if request.POST.get('post_identifier') == 'create' and request.user.is_active and request.user.is_authenticated():
            form = PostQuestionsForm(request.POST, request.FILES)
            if form.is_valid():
                return super().createNewGood(request, form)
            return self.get(request, form)
        return super().post(request)