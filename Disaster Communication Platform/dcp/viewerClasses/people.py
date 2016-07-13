from dcp.importUrls import *
from django.http.response import Http404
from django.template.context_processors import request
from django.shortcuts import get_object_or_404
from dcp.auth.generic import getListWithDelete
from braces.views import LoginRequiredMixin

class Suchen_Personen(LoginRequiredMixin,View):
	def get(self, request):
		profile = request.user.profile

		if profile.currentCatastrophe is not None:
			missed_people_raw = MissedPeople.objects.filter(catastrophe = profile.currentCatastrophe)
		else:
			missed_people_raw = MissedPeople.objects.all()

		form = MissedPeopleForm()
		characteristicsToUser = []
		for person in missed_people_raw:
			if person.characteristics:
				all_characteristics = person.characteristics.split(";")

				for c in all_characteristics:
					characteristicsToUser.append((c, person.id))

		missed_people = getListWithDelete(missed_people_raw, profile)

		template = 'dcp/content/suchen/personen.html'
		context = {'missed_people': missed_people, 'characteristicsToUser' : characteristicsToUser, 'form' : form}
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

	def post(self,request):
		template = 'dcp/content/suchen/personen.html'
		user = request.user
		if request.method == "POST":
			postIdentifier = request.POST.get('post_identifier')
			print(postIdentifier)
			if postIdentifier == 'create':
				form = MissedPeopleForm(request.POST)
				if form.is_valid():

					missed_person = MissedPeople(title=request.POST.get('title'),
					description=request.POST.get('description'),
					gender=request.POST.get('gender'),
					age=request.POST.get('age'),
					name=request.POST.get('name'),
					size=request.POST.get('size'),
					eyeColor=request.POST.get('eyeColor'),
					hairColor=request.POST.get('hairColor'),
					characteristics=request.POST.get('characteristics'),
					picture=request.FILES.get('picture'),
					user=request.user)

					missed_person.save()

					#person = form.save(commit=False)
					#person.user = request.user
					#person.save()

					url = reverse_lazy('dcp:Suchen_Personen')
					for u in User.objects.all():
						add_new_notification("Neue Person vermisst!", "Kennst du diese Person?", toUser=u, url=url)

					template = request.build_absolute_uri()
					return HttpResponseRedirect(template)
				else:
					raise Http404
			if postIdentifier == 'contact_form':
				person = get_object_or_404(MissedPeople, id=request.POST.get('missedpeople_id'))
				personOwner =  person.user
				user = request.user
				conv = Conversation.getConversationOrNone(userOne=user, userTwo=personOwner)
				if conv is None: # Wenn noch keine Conversation da ist
					Conversation.objects.create(Starter=user,Receiver=personOwner)
				url = '/chat/?userid='
				url += str(personOwner.id)
				return HttpResponseRedirect(url) # Jetzt: Redirect
			if postIdentifier == 'delete':
				person = get_object_or_404(MissedPeople, id=request.POST.get('missedpeople_id'))
				person.delete()
				template = request.build_absolute_uri()
				return HttpResponseRedirect(template)
			if postIdentifier == 'bump':
				user = request.user
				person = get_object_or_404(MissedPeople, id=request.POST.get('missedpeople_id'))
				bumps = person.bumps.filter(id=user.id)
				for placeholer in bumps:
					template = request.build_absolute_uri()
					return HttpResponseRedirect(template)
				person.bumps.add(user)
				template = request.build_absolute_uri()
				return HttpResponseRedirect(template)
			if postIdentifier == 'report':
				user = request.user
				person = get_object_or_404(MissedPeople, id=request.POST.get('missedpeople_id'))
				reports = person.reports.filter(id=user.id)
				for placeholer in reports:
					template = request.build_absolute_uri()
					return HttpResponseRedirect(template)
				person.reports.add(user)
				template = request.build_absolute_uri()
				return HttpResponseRedirect(template)


                #if people.bumps is None:
                #    people.bumps = Bump_Relation.objects.create()
                #    people.save()
                #else:
                #    already_exists = Bump.objects.filter(relation = good.bumps, user = user)
                #    if already_exists:
                #        template = request.build_absolute_uri()
                #        return HttpResponseRedirect(template)
                #relation = people.bumps
                #Bump.objects.create(user=user,relation=relation)

	def getMissedPeopleOr404(self, request):
		people = MissedPeople.get(id=request.POST.get('missedpeople_id'))
		if people is None:
			raise Http404
		return people
