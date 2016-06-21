from dcp.importUrls import *

class AktionenPlanung(View):
	def get(self, request):
		template = 'dcp/content/aktionen/planung.html'
		context = {}
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

	def post(self,request):
		template = 'dcp/content/aktionen/planung.html'
		return HttpResponseRedirect("/aktionen/planung/")


class AktionenLaufende(View):
	def get(self, request):
		template = 'dcp/content/aktionen/laufende.html'
		context = {}
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

	def post(self,request):
		template = 'dcp/content/aktionen/laufende.html'
		return HttpResponseRedirect("/aktionen/laufende/")		