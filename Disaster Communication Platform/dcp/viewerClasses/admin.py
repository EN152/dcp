# imports
from dcp.importUrls import *


class UserAdminOverview(views.SuperuserRequiredMixin,View):
    template = 'dcp/content/adminstrator/nutzer.html'
    def get(self,request):
        """
        :author: Vincent
        Zeigt - falls der User  ein Admin ist - alle Benutzer an und ermöglicht es dem Admin, Nutzer zu löschen
        """
        userList = User.objects.all()
        return render(request,self.template,context={'users': userList})

class CatastropheOverview(views.SuperuserRequiredMixin,View):
    template = 'dcp/content/adminstrator/catastropheOverview.html'
    def get(self,request):
        """
        :author Vincent
        Gibt eine Liste an Katastrohpen aus, mit der Möglichkeit Einträge zu löschen, Namen zu editieren und Katastrophen
        hinzuzufügen
        :param request:
        :return:
        """
        catastropheList = Catastrophe.objects.all()
        return render(request,self.template,context={'catastrophes':catastropheList})

class AdminEditUserProfileView(views.SuperuserRequiredMixin,UpdateView):
    fields = ['first_name', 'last_name', 'email']
    template_name = 'dcp/content/spezial/profilBearbeiten.html'
    model = User
    def get_success_url(self):
        return reverse('dcp:UserAdminOverview')

class DeleteUserView(views.SuperuserRequiredMixin,DeleteView):
    model = User
    template_name =  'dcp/content/adminstrator/deleteUser.html'
    def get_success_url(self):
        return reverse_lazy('dcp:UserAdminOverview')
