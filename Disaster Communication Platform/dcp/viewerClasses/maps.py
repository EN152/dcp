from dcp.importUrls import *

class Orte(LoginRequiredMixin,View):
    template = 'dcp/content/orte/orte.html'

    def get(self, request):
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template)

class Karten(View):
    template = 'dcp/content/orte/karten.html'

    def get(self, request):
        listOfGoods = []
        for oneGood in Search_Material.objects.all():
            url = reverse('dcp:SearchMaterialView')
            url += "#"+str(oneGood.id)
            listOfGoods.append((oneGood.location_x, oneGood.location_y, oneGood.title, oneGood.description,url))
        for oneGood in Offer_Immaterial.objects.all():
            url = reverse('dcp:OfferImmaterialView')
            url += "#"+str(oneGood.id)
            listOfGoods.append((oneGood.location_x, oneGood.location_y, oneGood.title, oneGood.description,url))
        for oneGood in Offer_Material.objects.all():
            url = reverse('dcp:OfferMaterialView')
            url += "#"+str(oneGood.id)
            listOfGoods.append((oneGood.location_x, oneGood.location_y, oneGood.title, oneGood.description,url))
        for oneGood in Search_Immaterial.objects.all():
            url = reverse('dcp:SearchImmaterialView')
            url += "#"+str(oneGood.id)
            listOfGoods.append((oneGood.location_x, oneGood.location_y, oneGood.title, oneGood.description,url))
        if request.user.is_authenticated():
            return render(request, self.template, {'goods': listOfGoods})
