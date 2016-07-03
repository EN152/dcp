from channels import Channel

from .imports import *
from dcp import dcpSettings
from django.utils import timezone

class Notification(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    toUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    noticed = models.BooleanField()
    pubdate = models.DateTimeField(default=timezone.now)

def add_new_notification(title,text,toUser):
    message = {'title':title,'text':text,'userid':toUser.id}
    Channel("notification-messages").send({"title": title, "text": text, "userid": toUser.id})
    #Notification.objects.create(title=title,text=text,toUser=toUser,noticed=False)


