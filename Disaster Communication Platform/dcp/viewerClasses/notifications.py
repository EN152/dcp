from dcp.importUrls import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
# models.notifications import *

class NotificationView(LoginRequiredMixin,View):
    templatePath = 'dcp/content/benachrichtigungen/notifications.html'

    def get(self,request):
        '''
        Zeige alle Notifications an
        :author Vincent
        :param request: --
        :return: --
        '''
        current_user = request.user;
        # Hole Notification für den user, die noch nicht als bemerkt gemarkt wurden
        notifications = Notification.objects.filter(toUser=current_user,noticed=False).order_by('pubdate')
        template = loader.get_template(self.templatePath)
        return HttpResponse(template.render({'notifications_list':notifications},request))
