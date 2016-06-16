# imports
from dcp.importUrls import *


def getPageAuthenticated(request, template, params={}):
    if request.user.is_authenticated():
        return render(request, template, params)
    else:
        return HttpResponseRedirect("/anmelden/")

class Register(View):
    template = 'dcp/content/spezial/anmelden.html'
    def post(self, request):
        if not request.user.is_authenticated():
            if request.method == "POST":
                username = request.POST['username']
                password = request.POST['password']
                email = request.POST['email']
                valid = bool(False)

                for users in User.objects.all():
                    if username == users.username:
                         return render(request, self.template, {'notVaild': valid})


                user = User.objects.create_user(username, email, password)
                user.save()
                return HttpResponseRedirect("/anmelden/")

class Login(View):
    template = 'dcp/content/spezial/anmelden.html'

    def get(self, request):
        catChoiceForm = CatastropheChoice
        return render(request, self.template, context={'catChoiceForm':catChoiceForm})
        
    def post(self, request):
       if request.method == "POST":
           username = request.POST['username']
           password = request.POST['password']
           catId = request.POST['catastrophe']

           valid = bool(False)
           user = authenticate(username=username, password=password)
           if user is not None:
               if user.is_active:
                   login(request, user)
                   Profile.get_profile_or_create(user).setCatastropheById(catId)
                   next = request.GET.get('next')
                   if next==None:
                       return HttpResponseRedirect("/")
                   else:
                       return HttpResponseRedirect(next)
               else:
                   return HttpResponse("Inactive user.")
           else:
               return render(request, self.template, {'notVaild': valid})
       return render(request, self.template, {})

class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("../anmelden/")