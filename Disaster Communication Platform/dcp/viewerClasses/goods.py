from dcp.customForms.goodsFroms import *
from dcp.viewerClasses.timeline import TimelineView
from dcp.viewerClasses.authentication import getPageAuthenticated
from dcp.views import View, LoginRequiredMixin
from dcp.auth.generic import isAllowedToDelete

class SearchMaterialView(TimelineView):
    def get(self, request, form=None, elementList=None):
        profile = request.user.profile
        if form is None:
            form = SearchMaterialForm      
        if elementList is None and profile.currentCatastrophe is None:
            elementList = Search_Material.objects.all().order_by('created_date').reverse()
        elif elementList is None:
            elementList = Search_Material.objects.filter(catastrophe=profile.currentCatastrophe).order_by('created_date').reverse()

        return super().getCreateNew(request, 'glyphicon-search', 'btn-primary' , 'Suchen: Materielles' , form, 'Search_Material', elementList)

    def post(self, request):
        if request.POST.get('post_identifier') == 'create' and request.user.is_active and request.user.is_authenticated():
            form = SearchMaterialForm(request.POST, request.FILES)
            if form.is_valid():
                return super().createNewGood(request, form)
            return self.get(request, form)
        return super().post(request)


class SearchImmaterialView(TimelineView):
    def get(self, request, form=None, elementList=None):
        profile = request.user.profile
        if form is None:
            form = SearchImmaterialForm

        if elementList is None and profile.currentCatastrophe is None:
            elementList = Search_Immaterial.objects.all().order_by('created_date').reverse()
        elif elementList is None:
            elementList = Search_Immaterial.objects.filter(catastrophe=profile.currentCatastrophe).order_by('created_date').reverse()

        return super().getCreateNew(request, 'glyphicon-search', 'btn-primary', 'Suchen: Immaterielles', form, 'Search_Immaterial', elementList=elementList)

    def post(self, request):
        if request.POST.get('post_identifier') == 'create' and request.user.is_active and request.user.is_authenticated():
            form = SearchImmaterialForm(request.POST, request.FILES)
            if form.is_valid():
                return super().createNewGood(request, form)
            return self.get(request, form)
        return super().post(request)


class OfferMaterialView(TimelineView):
    def get(self, request, form=None, elementList=None):
        profile = request.user.profile
        if form is None:
            form = OfferMaterialForm

        if elementList is None and profile.currentCatastrophe is None:
            elementList = Offer_Material.objects.all().order_by('created_date').reverse()
        elif elementList is None:
            elementList = Offer_Material.objects.filter(catastrophe=profile.currentCatastrophe).order_by('created_date').reverse()

        return super().getCreateNew(request, 'glyphicon-transfer', 'btn-danger', 'Bieten: Materielles', form, 'Offer_Material', elementList=elementList)

    def post(self, request):
        if request.POST.get('post_identifier') == 'create' and request.user.is_active and request.user.is_authenticated():
            form = OfferMaterialForm(request.POST, request.FILES)
            if form.is_valid():
                return super().createNewGood(request, form)
            return self.get(request, form)
        return super().post(request)


class OfferImmaterialView(TimelineView):
    def get(self, request, form=None, elementList=None):
        profile = request.user.profile
        if form is None:
            form = OfferImmaterialForm

        if elementList is None and profile.currentCatastrophe is None:
            elementList = Offer_Immaterial.objects.all().order_by('created_date').reverse()
        elif elementList is None:
            elementList = Offer_Immaterial.objects.filter(catastrophe=profile.currentCatastrophe).order_by('created_date').reverse()

        return super().getCreateNew(request, 'glyphicon-transfer', 'btn-danger', 'Bieten: Immaterielles', form, 'Offer_Immaterial', elementList=elementList)

    def post(self, request):
        if request.POST.get('post_identifier') == 'create' and request.user.is_active and request.user.is_authenticated():
            form = OfferImmaterialForm(request.POST, request.FILES)
            if form.is_valid():
                return super().createNewGood(request, form)
            return self.get(request, form)
        return super().post(request) 


class Bieten(LoginRequiredMixin, View):
    template = 'dcp/content/bieten/bieten.html'

    def get(self, request):
        return getPageAuthenticated(request, self.template)