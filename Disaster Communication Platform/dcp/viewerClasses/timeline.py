# imports
from dcp.customclasses.Helpers import url_with_querystring
from dcp.importUrls import *
from django.http import Http404
import dcp.dcpSettings
from django.template.context_processors import request
from django.template.backends.django import Template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import *
from geopy.geocoders import Nominatim
from dcp.auth.generic import getListWithDelete, isAllowedToDelete
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from dcp.models.goods import Goods


class TimelineView(LoginRequiredMixin, View):
    """ DOCS PENDING
    :author: Jasper
    """
    def post(self, request):
        user = request.user
        if user.is_authenticated() and user.is_active:
            postIdentifier = request.POST.get('post_identifier')
            if postIdentifier == 'comment':
                form = Comment_Form(request.POST)
                if form.is_valid():
                    text = request.POST.get('text')
                    if text is None or len(text) <= dcp.dcpSettings.MIN_COMMENT_LENGTH:
                        template = request.build_absolute_uri()
                        return HttpResponseRedirect(template)
                    good = self.get_good_or_404(request)
                    if good.comments is None:
                        good.comments = Comment_Relation.objects.create()
                        good.save()
                    relation = good.comments
                    Comment.objects.create(text=text,user=user,relation=relation)
                    template = request.build_absolute_uri()
                    return HttpResponseRedirect(template)

            if postIdentifier == 'contact_form':
                good = self.get_good_or_404(request)
                goodOwner =  good.user
                user = request.user
                # Schaue nach, ob schon eine Conv besteht..
                conv = Conversation.getConversationOrNone(userOne=user, userTwo=goodOwner)
                if conv is None: # Wenn noch keine Conversation da ist
                    Conversation.objects.create(Starter=user,Receiver=goodOwner)
                # Jetzt: Redirect
                url = url_with_querystring(reverse('dcp:ChatOverview'),userid=goodOwner.id)

                return HttpResponseRedirect(url)

            if postIdentifier == 'delete':
                good = self.get_good_or_404(request)
                if user.is_superuser or user == good.user or isAllowedToDelete(good.catastrophe, user.profile, good.location_x, good.location_y):
                    good.delete()
                    template = request.build_absolute_uri()
                    return HttpResponseRedirect(template)

            if postIdentifier == 'bump':
                good = self.get_good_or_404(request)
                if good.bumps is None:
                    good.bumps = Bump_Relation.objects.create()
                    good.save()
                else:
                    already_exists = Bump.objects.filter(relation = good.bumps, user = user)
                    if already_exists:
                        template = request.build_absolute_uri()
                        return HttpResponseRedirect(template)
                relation = good.bumps
                Bump.objects.create(user=user,relation=relation)
                template = request.build_absolute_uri()
                return HttpResponseRedirect(template)

            if postIdentifier == 'report':
                good = self.get_good_or_404(request)
                if user == good.user:
                    return HttpResponseForbidden('You cannot report yourself')
                relation = None
                if good.reports is None:
                    good.reports = Report_Relation.objects.create()
                    good.save()
                else:
                    already_exists = Report.objects.filter(relation = good.reports, user = user)
                    if already_exists:
                        template = request.build_absolute_uri()
                        return HttpResponseRedirect(template)
                relation = good.reports
                Report.objects.create(user=user,relation=relation)
                template = request.build_absolute_uri()
                return HttpResponseRedirect(template)
        return Http404

    def getCreateNew(self, request, create_new_glyphicon, create_new_button, page_title, create_new_form, good_typ, elementList=None):
        templatePath = 'dcp/content/createNewGood.html'
        if elementList is None:
            # Legacy
            elementList = sorted(Goods.getAllGoods(), key=lambda g: g.created_date, reverse=True)
            elementList = filter(lambda x: type(x) is eval(good_typ), elementList)

        goods_list = getListWithDelete(elementList, request.user.profile)

        categoryForm = CategoryFilterForm()
        template = loader.get_template(templatePath)
        categoryChoices = CategorysGoods.objects.all()
        context = {
            'create_new_glyphicon': create_new_glyphicon,
            'create_new_button' : create_new_button,
            'page_title': page_title,
            'create_new_form' : create_new_form,
            'goods_list' : goods_list,
            #'categoryfilterform': categoryForm,
            'categoryChoices' : categoryChoices
        }

        return HttpResponse(template.render(context,request))

    def createNewGood(self, request, form):
        if form.is_valid():
            newGood = form.save(commit=False)
            newGood.user = request.user
            if newGood.location_x == 0 and newGood.location_y == 0:
                newGood.location_x = None
                newGood.location_y = None
            else:
                try :
                    geolocator = Nominatim()
                    location = geolocator.reverse(str(newGood.location_x) + " , " + str(newGood.location_y))
                    newGood.locationString = location.address
                except :
                    newGood.locationString = ""
            newGood.save()
            template = request.build_absolute_uri()
            return HttpResponseRedirect(template)
        raise Http404

    def get_good_or_404(self, request):
        good = Goods.getGood(request.POST.get('good_type'), request.POST.get('good_id'))
        if good is None:
           raise Http404
        return good

class TimelineManagerView(TimelineView):

    def get(self, request):
        templatePath = 'dcp/content/adminstrator/timelineManager.html'
        template = loader.get_template(templatePath)
        reportList = []
        goodList = Goods.getAllGoods()
        for good in goodList:
            reportCount = good.getReports().count()
            if(reportCount >= dcpSettings.REPORT_COUNT):
                reportList.append(good)

        goods_list = getListWithDelete(reportList, request.user.profile)

        return HttpResponse(template.render({"goods_list" : goods_list},request))

    def post(self, request):
        super().post(request)
        return self.get(request)

