# imports
from dcp.importUrls import *

class MyProfile(View):
    template = 'dcp/content/spezial/profil.html'
           
    def get(self, request):
        return getPageAuthenticated(request, self.template)
        
class EditProfile(View):
    template = 'dcp/content/spezial/profilBearbeiten.html'
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        form = UserForm(initial={'email' : user.email,'first_name': user.first_name,'last_name':user.last_name,'password':''})
        return getPageAuthenticated(request, self.template, {'form': form})
    def post(self,request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = User.objects.get(username=request.user.username)
                email = request.POST.get("email")
                password = request.POST.get("password")
                scndpwd = request.POST.get("scndpwd")
                if email != None: # Der Nutzer will die Email ändern
                    user.email = email
                    user.save()
                if password != None and password != scndpwd:
                    messages.add_message(request, messages.INFO,'Passwörter nicht identisch')
                    return render(request, self.template, {'form': form})
                else:
                    user.set_password(password)
                    user.save()
                    return HttpResponseRedirect("/profil/")
        return HttpResponseRedirect("/profil/")




