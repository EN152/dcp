# imports
from dcp.importUrls import *


def getPageAuthenticated(request, template, params={}):
    if request.user.is_authenticated():
        return render(request, template, params)
    else:
        return HttpResponseRedirect("/anmelden/")

class RegisterView(View):
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
                         return render(request, self.template, {'notAvailable': valid})


                user = User.objects.create_user(username, email, password)
                user.save()
                return HttpResponseRedirect("/anmelden/")

class LoginView(View):
    def get(self, request, context={}):
        templatePath = 'dcp/content/spezial/anmelden.html'
        template = loader.get_template(templatePath)
        return HttpResponse(template.render(context=context, request=request))
        
    def post(self, request):
       template = 'dcp/content/spezial/anmelden.html'
       username = request.POST.get('username')
       password = request.POST.get('password')

       user = authenticate(username=username, password=password)
       if user is not None:
           if user.is_active:
               login(request, user)
               Profile.get_profile_or_create(user)
               next = request.GET.get('next')
               if next==None:
                   return HttpResponseRedirect("/")
               else:
                   return HttpResponseRedirect(next)
           else:
               return HttpResponse("Inactive user.")
       else:
        return self.get(request, context={'notValid': True})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/anmelden/")