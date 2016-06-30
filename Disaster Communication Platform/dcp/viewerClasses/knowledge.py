from dcp.customForms.goodsFroms import *
from dcp.viewerClasses.timeline import TimelineView
from dcp.viewerClasses.authentication import getPageAuthenticated
from dcp.views import View, LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from dcp.models.catastrophe import *
from dcp.models.profile import *

class Wissen(LoginRequiredMixin,View):
    template = 'dcp/content/wissen/wissen.html'

    def get(self, request):
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template)
