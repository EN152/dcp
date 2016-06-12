from dcp.importUrls import *

class Suchen_Personen(View):
	def get(self, request):
		missed_people = MissedPeople.objects.all()
		form = MissedPeopleForm()

		characteristicsToUser = []
		for person in missed_people:
			if person.characteristics:
				all_characteristics = person.characteristics.split(";")
				
				for c in all_characteristics:
					characteristicsToUser.append((c, person.title))

		template = 'dcp/content/suchen/personen.html'
		context = {'missed_people': missed_people, 'characteristicsToUser' : characteristicsToUser, 'form' : form}
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

	def post(self,request):
		template = 'dcp/content/suchen/personen.html'
		if request.method == "POST":
			form = MissedPeopleForm(request.POST)
			if form.is_valid():
				missed_person = MissedPeople(title=request.POST['title'], 
					description=request.POST['description'], 
					gender=request.POST['gender'], 
					age=request.POST['age'], 
					name=request.POST['name'], 
					size=request.POST['size'], 
					eyeColor=request.POST['eyeColor'], 
					hairColor=request.POST['hairColor'], 
					characteristics=request.POST['characteristics'],
					picture=request.POST['picture'],
					user=request.user)
					# catastrophe=Catastrophe.objects.get(id=1) # TODO: replace with real catastrophe id!
				missed_person.save()
		return HttpResponseRedirect("/suchen/personen/")