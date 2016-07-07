from dcp.importUrls import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import  Q
from django.core.urlresolvers import reverse
from dcp.models import *

class NotificationView(LoginRequiredMixin,View):
    templatePath = 'dcp/content/benachrichtigungen/notifications.html'

    def get(self,request):
        '''
        Zeige alle Notifications an
        :author Vincent
        :param request: --
        :return: --
        '''
        current_user = request.user #type:User
        template = loader.get_template(self.templatePath)
        # Hole Notification für den user, die noch nicht als bemerkt gemarkt wurden
        notifications = get_notifications(current_user)
        return HttpResponse(template.render({'notifications_list':notifications},request))

