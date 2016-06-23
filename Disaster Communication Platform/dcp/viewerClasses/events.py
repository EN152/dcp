from dcp.importUrls import *

class AktionenPlanung(View):
	def get(self, request):
		template = 'dcp/content/aktionen/planung.html'

		rawEvents = Event.objects.all()
		# this step creates an n-tuple because range() cannot be used in template and many-to-many is not iterable
		events = []
		for event in rawEvents:
			numberOfRows = max((event.numberOfUsers, event.numberOfCars, event.numberOfSpecials))
			nameOfCurrentUser = request.user.username	
			
			numberOfMembers = event.members.count()
			namesOfMembers = []
			for member in event.members.all():
				namesOfMembers.append(member.username)
		
			numberOfCars = event.cars.count()
			descriptionsOfCars = []
			for car in event.cars.all():
				descriptionsOfCars.append(car.description)

			usernamesOfCars = []
			for car in event.cars.all():
				descriptionsOfCars.append(car.owner.username)

			idsOfCars = []
			for car in event.cars.all():
				descriptionsOfCars.append(car.id)		
			
			numberOfSpecials = event.specials.count()
			descriptionsOfSpecials = []
			for special in event.specials.all():
				descriptionsOfSpecials.append((special.description, special.owner.username))

			userIsMemberOfCurrentEvent = False
			if request.user in event.members.all():
				userIsMemberOfCurrentEvent = True

			
			usernamesOfCars = []
			for car in event.cars.all():
				descriptionsOfCars.append((car.description, car.owner.username, car.id))	
	
			#0: event
			#1: range(numberOfRows)
			#2: numberOfMembers
			#3: namesOfMembers
			#4: userIsMemberOfCurrentEvent
			#5: nameOfCurrentUser
			#6: numberOfCars
			#7: descriptionsOfCars
			#8: numberOfSpecials
			#9: descriptionsOfSpecials
			# 10: usernamesOfCars
			# 11: idsOfCars
			events.append((event, range(numberOfRows), numberOfMembers, namesOfMembers, userIsMemberOfCurrentEvent, nameOfCurrentUser, numberOfCars, descriptionsOfCars, numberOfSpecials, descriptionsOfSpecials, usernamesOfCars, idsOfCars))

		context = {'events' : events}
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

	def post(self,request):
		template = 'dcp/content/aktionen/planung.html'

		user = request.user
		event_id = request.POST.get('event_id')
		event = Event.objects.get(id=event_id)
		
		if event is None:
			context = {'error': 'Da ist leider etwas schief gelaufen! :('}
			return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)


		if request.POST.get('post_identifier') == 'add_user' and request.user.is_active and request.user.is_authenticated():
			if user in event.members.all():
				context = {'error': 'Du hast dich bei diesem Event bereits eingetragen!'}
				return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

			event.members.add(user)
			event.save()
		
		if request.POST.get('post_identifier') == 'remove_user' and request.user.is_active and request.user.is_authenticated():
			event.members.remove(user)
			event.save()


		if request.POST.get('post_identifier') == 'add_car' and request.user.is_active and request.user.is_authenticated():
			car_description = request.POST.get('car_description')
			car = Car.objects.create(description=car_description, owner=user)
			event.cars.add(car)
			event.save()
		
		if request.POST.get('post_identifier') == 'remove_car' and request.user.is_active and request.user.is_authenticated():
			car_id = request.POST.get('car_id')
			car = Car.objects.get(id=car_id)
			if car.owner == user:
				event.cars.remove(car)
				event.save()
			else:
				context = {'error': 'Hallo!? Das war gar nicht dein Auto! :('}
				return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)


		return HttpResponseRedirect('/aktionen/planung')

		


class AktionenLaufende(View):
	def get(self, request):
		template = 'dcp/content/aktionen/laufende.html'
		context = {}
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

	def post(self,request):
		template = 'dcp/content/aktionen/laufende.html'
		return HttpResponseRedirect("/aktionen/laufende/")