# imports
from dcp.importUrls import *

class WordSearch(View):
    searchString = ""
    templatePath = 'dcp/content/suchen/wortsuche.html'

    def get(self,request):
        self.searchString = request.GET.get("searchText")
        if self.searchString == None:
            # handle if it's none
            return HttpResponse("None")
        else:
            goods_list = sorted(Goods.getAllGoods(), key=lambda g: g.created_date, reverse=True)
            searched_goods_list = [g for g in goods_list if g.isSearchedForByString(self.searchString)]
            total_search_materials = len([g for g in searched_goods_list if g.getGoodType() == 'Search_Material' or g.getGoodType() == 'Search_Immaterial'])
            total_offer_materials = len([g for g in searched_goods_list if g.getGoodType() == 'Offer_Material' or g.getGoodType() == 'Offer_Immaterial'])

            context = {'searchString':self.searchString,
            'goods_list':searched_goods_list,
            'goods_list_size':len(searched_goods_list),
            'total_search_materials':total_search_materials,
            'total_offer_materials':total_offer_materials}

            template = loader.get_template(self.templatePath)
            return HttpResponse(template.render(context,request))