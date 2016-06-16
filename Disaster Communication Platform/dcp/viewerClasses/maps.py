from dcp.importUrls import *

class Karten(View):
    template = 'dcp/content/orte/karten.html'

    def get(self, request):
        listOfGoods = []
        for oneGood in Search_Material.objects.all():
            listOfGoods.append((oneGood.location_x, oneGood.location_y, oneGood.title, oneGood.description))
        for oneGood in Offer_Immaterial.objects.all():
            listOfGoods.append((oneGood.location_x, oneGood.location_y, oneGood.title, oneGood.description))
        for oneGood in Offer_Material.objects.all():
            listOfGoods.append((oneGood.location_x, oneGood.location_y, oneGood.title, oneGood.description))
        for oneGood in Search_Immaterial.objects.all():
            listOfGoods.append((oneGood.location_x, oneGood.location_y, oneGood.title, oneGood.description))
        if request.user.is_authenticated():
            return render(request, self.template, {'goods': listOfGoods})