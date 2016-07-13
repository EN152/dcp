# imports
from dcp.importUrls import *
from dcp.customForms.LoginForms import LoginForm, RegisterForm


def getPageAuthenticated(request, template, params={}):
    if request.user.is_authenticated():
        return render(request, template, params)
    else:
        return HttpResponseRedirect("/anmelden/")

class LoginView(View):
    def get(self, request, loginForm=LoginForm, registerForm=RegisterForm):
        templatePath = 'dcp/content/spezial/anmelden.html'
        template = loader.get_template(templatePath)
        context = {
            'loginForm' : loginForm,
            'registerForm' : registerForm
        }

        return HttpResponse(template.render(context=context, request=request))
        
    def post(self, request):
        post_identifier = request.POST.get('post_identifier')
        if post_identifier == 'login':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
                if user is not None and user.is_active:
                     login(request, user)
                     Profile.get_profile_or_create(user)
                     return HttpResponseRedirect("/")
                else :
                     form.add_error('password', 'Die Kombination aus Passwort und Nutzername wurde nicht erkannt')
                     form.add_error('username', '')
            
            return self.get(request, loginForm=form)
        if post_identifier == 'register':
            if not request.user.is_authenticated():
                form = RegisterForm(request.POST)
                if form.is_valid():
                    user = User.objects.create_user(form.cleaned_data.get('username'), form.cleaned_data.get('email'), form.cleaned_data.get('password'))
                    user.save()
                    user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
                    Profile.get_profile_or_create(user=user)
                    login(request, user)
                    return HttpResponseRedirect("/")
            return self.get(request, registerForm=form)
        return self.get(request)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/anmelden/")