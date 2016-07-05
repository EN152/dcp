# imports
from dcp.importUrls import *
from dcp.viewerClasses.timeline import *
from dcp.auth.generic import getListWithDelete

class Index(TimelineView):
    def get(self, request):
        templatePath = 'dcp/index.html'
        template = loader.get_template(templatePath)
        panel_title = "Übersicht  deiner erstellten Gesuche und Angebote"

        countSearch = len(dcp.models.Search_Material.objects.all()) + len(dcp.models.Search_Immaterial.objects.all())
        countOffer = len(dcp.models.Offer_Material.objects.all()) + len(dcp.models.Offer_Immaterial.objects.all())
        countInformation = 0 # TODO
        countPeople = len(MissedPeople.objects.all())

        user = request.user
        profile = user.profile
        if profile.currentCatastrophe is not None:
            goods_list = Goods.getAllGoods(user=user, catastrophe=profile.currentCatastrophe)#, key=lambda g: g.created_date, reverse=True)
        else :
            goods_list = Goods.getAllGoods(user=user)
        goods_list = Goods.sortByBumpCount(goods_list)
        goods_list = getListWithDelete(goods_list, profile)
        quickstart = False
        count_sum = countSearch + countOffer + countInformation + countPeople
        if count_sum < 1:
        	quickstart = True       
        
        context = {
        		'goods_list': goods_list,
        		'quickstart' : quickstart,
        		'countSearch': countSearch,
        		'countOffer': countOffer,
        		'countInformation': countInformation,
        		'countPeople': countPeople,
        		'panel_title': panel_title
        }
        return HttpResponse(template.render(context, request))

    def post(self, request):
        return super().post(request)
