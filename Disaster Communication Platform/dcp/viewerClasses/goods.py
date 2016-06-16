# imports
from dcp.importUrls import *

class SearchMaterialView(dcp.viewerClasses.timeline.TimelineView):
    def get(self, request):
        return super().getCreateNew(request, 'Search_Material', True, 'glyphicon-search', 'Suchen: Materielles')

    def post(self, request):
        return super().post(request)


class SearchImmaterialView(dcp.viewerClasses.timeline.TimelineView):
    def get(self, request):
        return super().getCreateNew(request, 'Search_Immaterial', True, 'glyphicon-search', 'Suchen: Immaterielles')

    def post(self, request):
        return super().post(request)


class OfferMaterialView(dcp.viewerClasses.timeline.TimelineView):
    def get(self, request):
        return super().getCreateNew(request, 'Offer_Material', False, 'glyphicon-transfer', 'Bieten: Materielles')

    def post(self, request):
        return super().post(request)


class OfferImmaterialView(dcp.viewerClasses.timeline.TimelineView):
    def get(self, request):
        return super().getCreateNew(request, 'Offer_Immaterial', False, 'glyphicon-transfer', 'Bieten: Immaterielles')

    def post(self, request):
        return super().post(request)


class Bieten(LoginRequiredMixin, View):
    template = 'dcp/content/bieten/bieten.html'

    def get(self, request):
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template)