from dcp.importUrls import *
from dcp.auth.generic import isAllowedToDelete
from dcp.customclasses.Helpers import url_with_querystring

class Aktionen(View):
	template = 'dcp/content/aktionen/aktionen.html'
	def get(self, request):
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template)

class AktionenPlanung(View):
	def get(self, request):
		template = 'dcp/content/aktionen/planung.html'
		form = EventPlanningForm()
		context = {'form' : form}
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

	def post(self,request):
		form = EventPlanningForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			description = form.cleaned_data['description']
			begin_date = form.cleaned_data['begin_date']
			numberofUsers = form.cleaned_data['numberOfUsers']
			numberofCars = form.cleaned_data['numberOfCars']
			numberofSpecial = form.cleaned_data['numberOfSpecials']
			catastrophe = form.cleaned_data['catastrophe']
		else:
			template = 'dcp/content/aktionen/planung.html'
			context = {'form': form}
			return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)
		event = Event.objects.create(title=title,
			description=description,
			begin_date =begin_date,
			numberOfUsers = numberofUsers,
			numberOfCars = numberofCars,
			numberOfSpecials = numberofSpecial,
			catastrophe = catastrophe,createdby=request.user)
		event.members.add(request.user)
		event.save()
		return HttpResponseRedirect('/aktionen/laufende/#' + str(event.id))

class AktionenLaufende(View):
	def get(self, request):
		template = 'dcp/content/aktionen/laufende.html'

		rawEvents = Event.objects.all()

		if len(rawEvents) == 0:
			error = 'Leider gibt es noch keine Aktionen! :('
			context = {'error' : error }
			return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

		# this step creates an n-tuple because range() cannot be used in template
		# and many-to-many objects are not iterable...and I didn't want to pass >10 single objects...

		events = []
		for event in rawEvents:
			current_user_allowed_to_delete = isAllowedToDelete(catastrophe=event.catastrophe,profile=request.user.profile) or (event.createdby==request.user)
			numberOfRows = max((event.numberOfUsers, event.numberOfCars, event.numberOfSpecials))
			nameOfCurrentUser = request.user.username

			userIsMemberOfCurrentEvent = False
			if request.user in event.members.all():
				userIsMemberOfCurrentEvent = True

			# people
			numberOfMembers = event.members.count()

			namesOfMembers = []
			for member in event.members.all():
				namesOfMembers.append(member.username)


			#cars
			numberOfCars = event.cars.count()

			descriptionsOfCars = []
			usernamesOfCars = []
			idsOfCars = []
			for car in event.cars.all():
				descriptionsOfCars.append(car.description)
				usernamesOfCars.append(car.owner.username)
				idsOfCars.append(car.id)


			# specials
			numberOfSpecials = event.specials.count()

			descriptionsOfSpecials = []
			usernamesOfSpecials = []
			idsOfSpecials = []
			for special in event.specials.all():
				descriptionsOfSpecials.append(special.description)
				usernamesOfSpecials.append(special.owner.username)
				idsOfSpecials.append(special.id)

				# 00: event
				# 01: range(numberOfRows)
				# 02: numberOfMembers
				# 03: namesOfMembers
				# 04: userIsMemberOfCurrentEvent
				# 05: nameOfCurrentUser
				# 06: numberOfCars
				# 07: descriptionsOfCars
				# 08: numberOfSpecials
				# 09: descriptionsOfSpecials
				# 10: usernamesOfCars
				# 11: idsOfCars
				# 12: usernamesOfSpecials
				# 13: idsOfSpecials
				# 14: current_user_allowed_to_delete
			events.append((event, range(numberOfRows), numberOfMembers,
				namesOfMembers, userIsMemberOfCurrentEvent,
				nameOfCurrentUser, numberOfCars, descriptionsOfCars,
				numberOfSpecials, descriptionsOfSpecials, usernamesOfCars,
				idsOfCars, usernamesOfSpecials, idsOfSpecials, current_user_allowed_to_delete))

		context = {'events' : events,'deleteeventform':DeleteEventForm()}
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

	def post(self,request):
		template = 'dcp/content/aktionen/laufende.html'
		
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

			url = reverse_lazy('dcp:EventsView') + '#' + str(event.id)
			for m in event.members.all():
				add_new_notification("Neuer Teilnehmer", m.username + " nimmt an der Veranstaltung teil!", toUser=m, url=url)

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

		if request.POST.get('post_identifier') == 'add_special' and request.user.is_active and request.user.is_authenticated():
			special_description = request.POST.get('special_description')
			special = Special.objects.create(description=special_description, owner=user)
			event.specials.add(special)
			event.save()

		if request.POST.get('post_identifier') == 'remove_special' and request.user.is_active and request.user.is_authenticated():
			special_id = request.POST.get('special_id')
			special = Special.objects.get(id=special_id)
			if special.owner == user:
				event.specials.remove(special)
				event.save()
			else:
				context = {'error': 'Hallo!? Das war gar nicht dein besonderer Gegenstand! :('}
				return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)
		if request.POST.get('post_identifier') == 'delete':
			form = DeleteEventForm(request.POST,instance=event)
			if form.is_valid():
				if (isAllowedToDelete(catastrophe=event.catastrophe,profile=request.user.profile) or (event.createdby==request.user)):
					event.delete()
					return  HttpResponseRedirect(reverse_lazy('dcp:EventsView'))

		# ...mit #id springt man direkt wieder zum Event, das man gerade bearbeitet hat :)
		return HttpResponseRedirect('/aktionen/laufende/#' + str(event.id))
