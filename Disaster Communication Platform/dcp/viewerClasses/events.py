from dcp.importUrls import *

class AktionenPlanung(View):
	def get(self, request):
		template = 'dcp/content/aktionen/planung.html'

		rawEvents = Event.objects.all()
		# this step creates an n-tuple because range() cannot be used in template and int is not iterable
		events = []
		for event in rawEvents:
			numberOfRows = max((event.numberOfUsers, event.numberOfCars, event.numberOfSpecials))
			numberOfMembers = event.members.count()
			
			namesOfMembers = []
			for member in event.members.all():
				namesOfMembers.append(member.username)
		
			userIsMemberOfCurrentEvent = False
			if request.user in event.members.all():
				userIsMemberOfCurrentEvent = True
		
			nameOfCurrentUser = request.user.username	
			events.append((event, range(numberOfRows), numberOfMembers, namesOfMembers, userIsMemberOfCurrentEvent, nameOfCurrentUser))

		context = {'events' : events}
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

	def post(self,request):
		template = 'dcp/content/aktionen/planung.html'

		if request.POST.get('post_identifier') == 'add_user' and request.user.is_active and request.user.is_authenticated():
			event_id = request.POST.get('event_id')
			user = request.user

			event = Event.objects.get(id=event_id)
			if event is None:
				context = {'error': 'Da ist leider etwas schief gelaufen! :('}
				return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)
			
			if user in event.members.all():
				context = {'error': 'Du hast dich bei diesem Event bereits eingetragen!'}
				return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

			event.members.add(user)
			event.save()
		
		if request.POST.get('post_identifier') == 'remove_user' and request.user.is_active and request.user.is_authenticated():
			event_id = request.POST.get('event_id')
			user = request.user

			event = Event.objects.get(id=event_id)
			if event is None:
				context = {'error': 'Da ist leider etwas schief gelaufen! :('}
				return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)
			
			event.members.remove(user)
			event.save()

		return HttpResponseRedirect('/aktionen/planung')

		


class AktionenLaufende(View):
	def get(self, request):
		template = 'dcp/content/aktionen/laufende.html'
		context = {}
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

	def post(self,request):
		template = 'dcp/content/aktionen/laufende.html'
		return HttpResponseRedirect("/aktionen/laufende/")