from channels import Channel

from .imports import *
from dcp import dcpSettings
from django.utils import timezone

class Notification(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    toUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='customNotifications')
    noticedBy = models.ManyToManyField(User,related_name='noticedNotifications')
    pubdate = models.DateTimeField(default=timezone.now)
    url = models.CharField(max_length=256,null=True)
#class UserHasNoticed(models.Model):
#    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
#    notification = models.ForeignKey(Notification,on_delete=models.CASCADE,null=False)
def add_new_notification(title,text,toUser=None,url=None):
    """
    Füge eine neue Benachrichtungen an einen bestimmten User oder alle User hinzu
    :author Vincent
    :param title: Der Titel der Benachrichtigung
    :param text: Der Text der Benachrichtigung
    :param toUser: None, falls die Benachrichtigung an alle gehen soll, sonst  eine bestimmte Benutzerinstanz
    :param url: None, falls keine URL, sonst die URL, die beim Klicken der Benachrichtigung aufgerufen werden sollen
    :return: --
    """
    message = {'title':title,'text':text}
    if toUser is not None:
        message['userid'] = toUser.id
        Channel("notification-messages").send({"title": title, "text": text, "userid": toUser.id,'url':url})
    else:
        Channel("notification-messages").send({"title":title,"text":text,'url':url})
    #Notification.objects.create(title=title,text=text,toUser=toUser,noticed=False)


