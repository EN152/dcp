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
        current_user = request.user;
        template = loader.get_template(self.templatePath)
        # Hole Notification für den user, die noch nicht als bemerkt gemarkt wurden
        notifications = Notification.objects.filter(Q(toUser=current_user,noticed=False) | Q(toUser=None)).exclude(id__in = UserHasNoticed.objects.filter(user=current_user).values_list('id',flat=True)).order_by('-pubdate')
        return HttpResponse(template.render({'notifications_list':notifications},request))

