from dcp.importUrls import *

class AktionenPlanung(View):
	def get(self, request):
		template = 'dcp/content/aktionen/planung.html'

		allEvents = Event.objects.all()

	
#		table_headings = []
#		numberOfUsers = 5
#		user_icon = 'fa fa-user'
#
#		numberOfCars = 2
#		car_icon = 'fa fa-car'
#
#		numberOfSpecials = 2
#		special_icon = 'fa fa-star'
#
#		for i in range(0,numberOfUsers):
#			table_headings += [user_icon]
#		
#		for i in range(0,numberOfCars):
#			table_headings += [car_icon]
#
#		for i in range(0,numberOfSpecials):
#			table_headings += [special_icon]	
	

		context = {'events' : allEvents}
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

	def post(self,request):
		template = 'dcp/content/aktionen/planung.html'
		return HttpResponseRedirect("/aktionen/planung/")

#	def addTableHeading(table_headings, nb, icon):
#		if table_headings.size == 0 or nb == 0 or icon == '':
#			return []
#
#		table_headings = table_headings
#		for i in range(0,nb):
#			table_headings += [icon]
#		return table_headings			


class AktionenLaufende(View):
	def get(self, request):
		template = 'dcp/content/aktionen/laufende.html'
		context = {}
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

	def post(self,request):
		template = 'dcp/content/aktionen/laufende.html'
		return HttpResponseRedirect("/aktionen/laufende/")