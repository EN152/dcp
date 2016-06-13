# imports
from dcp.importUrls import *

class Index(View):

	def get(self, request):
		countSearch = -1
		countOffer = -1
		countInformation = -1
		countPeople = len(MissedPeople.objects.all())
		
		# user = request.user und irgendwas wie .filter(user=user) fehlt noch...
		goods_list = sorted(Goods.getAllGoods(), key=lambda g: g.created_date, reverse=True)
		category_glyphicon_list = Categorys.getCategoryListAsGlyphiconString()
		category_name_list = Categorys.getCategoryListAsNameString()

		category_list = zip(category_glyphicon_list, category_name_list)

		template = 'dcp/index.html'
		params = {
				'goods_list': goods_list,
				'category_list' : category_list,
				'countSearch': countSearch,
				'countOffer': countOffer,
				'countInformation': countInformation,
				'countPeople': countPeople
		}
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, params)

	def post(self, request):
		self.params += request.user

		if request.user.is_authenticated():
			return HttpResponseRedirect("")
		else:
			return HttpResponseRedirect("anmelden/")