# imports
from dcp.importUrls import *
from django.http import Http404

class SearchMaterialView(dcp.viewerClasses.timeline.TimelineView):
    def get(self, request):
        return super().getCreateNew(request, 'Search_Material', True, True, 'glyphicon-search', 'Suchen: Materielles')

    def post(self, request):
        if request.POST.get('post_identifier') == 'create' and request.user.is_active and request.user.is_authenticated():
            radius = request.POST.get('radius')
            try:
                radiusSplit = radius.split(' ')
                radius = radiusSplit[0]
            except:
                raise Http404
            title = request.POST.get('title')
            description = request.POST.get('description')
            catastrophe = get_object_or_404(Catastrophe, id=request.POST.get('catastrophe'))
            location_x = request.POST.get('location_x')
            location_y = request.POST.get('location_y')
            categoryString = request.POST.get('category')
            category = Categorys.stringToCategoryTypeAsNumber(categoryString)
            if radius is None or title is None or catastrophe is None or location_x is None or location_y is None or category is None:
                raise Http404 
            Search_Material.objects.create(title=title, description=description, radius=radius, catastrophe=catastrophe, location_x=location_x, location_y=location_y, category=category, user=request.user)
            return HttpResponseRedirect('')
        return super().post(request)


class SearchImmaterialView(dcp.viewerClasses.timeline.TimelineView):
    def get(self, request):
        return super().getCreateNew(request, 'Search_Immaterial', True, False, 'glyphicon-search', 'Suchen: Immaterielles')

    def post(self, request):
        if request.POST.get('post_identifier') == 'create' and request.user.is_active and request.user.is_authenticated():
            radius = request.POST.get('radius')
            try:
                radiusSplit = radius.split(' ')
                radius = radiusSplit[0]
            except:
                raise Http404
            title = request.POST.get('title')
            description = request.POST.get('description')
            catastrophe = get_object_or_404(Catastrophe, id=request.POST.get('catastrophe'))
            location_x = request.POST.get('location_x')
            location_y = request.POST.get('location_y')
            if radius is None or title is None or catastrophe is None or location_x is None or location_y is None:
                raise Http404
            Search_Immaterial.objects.create(title=title, description=description, radius=radius, catastrophe=catastrophe, location_x=location_x, location_y=location_y, user=request.user)
            return HttpResponseRedirect('')
        return super().post(request)


class OfferMaterialView(dcp.viewerClasses.timeline.TimelineView):
    def get(self, request):
        return super().getCreateNew(request, 'Offer_Material', False, True, 'glyphicon-transfer', 'Bieten: Materielles')

    def post(self, request):
        if request.POST.get('post_identifier') == 'create' and request.user.is_active and request.user.is_authenticated():
            title = request.POST.get('title')
            description = request.POST.get('description')
            catastrophe = get_object_or_404(Catastrophe, id=request.POST.get('catastrophe'))
            location_x = request.POST.get('location_x')
            location_y = request.POST.get('location_y')
            categoryString = request.POST.get('category')
            category = Categorys.stringToCategoryTypeAsNumber(categoryString)
            if title is None or catastrophe is None or location_x is None or location_y is None or category is None:
                raise Http404 
            Offer_Material.objects.create(title=title, description=description, catastrophe=catastrophe, location_x=location_x, location_y=location_y, category=category, user=request.user)
            return HttpResponseRedirect('')
        return super().post(request)


class OfferImmaterialView(dcp.viewerClasses.timeline.TimelineView):
    def get(self, request):
        return super().getCreateNew(request, 'Offer_Immaterial', False, False, 'glyphicon-transfer', 'Bieten: Immaterielles')

    def post(self, request):
        if request.POST.get('post_identifier') == 'create' and request.user.is_active and request.user.is_authenticated():
            title = request.POST.get('title')
            description = request.POST.get('description')
            catastrophe = get_object_or_404(Catastrophe, id=request.POST.get('catastrophe'))
            location_x = request.POST.get('location_x')
            location_y = request.POST.get('location_y')
            if title is None or  catastrophe is None or location_x is None or location_y is None:
                raise Http404
            Offer_Immaterial.objects.create(title=title, description=description, catastrophe=catastrophe, location_x=location_x, location_y=location_y, user=request.user)
            return HttpResponseRedirect('')
        return super().post(request)      


class Bieten(LoginRequiredMixin, View):
    template = 'dcp/content/bieten/bieten.html'

    def get(self, request):
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template)