from .imports import *
from dcp.customclasses import Helpers
class Conversation(models.Model):
    Starter  = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='Starter')
    Receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='Receiver')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('Starter','Receiver')
    def getConversationOrNone(userOne: User,userTwo: User):
        """
        Schaut nach, ob bereits eine Konversation zwischen zwei Nutzern
        in der Datenbank gespeichert ist. Falls ja wird die Konversation zurückgegeben,
        sonst None. Auf die Reihenfolge der Nutzer wird nicht geachtet, es
        ist also egal wer die Konversation tatsächlich gestartet hat
        :author Vincent
        :param userone: Chatteilnehmer1
        :param usertwo: Chatteilnehmer2
        :return: Konversation falls existent, sonst None
        """
        conversation = Helpers.get_object_or_none(Conversation,
                                                                         Starter=userOne,
                                                                         Receiver=userTwo)

        if conversation is None:
            conversation = Helpers.get_object_or_none(Conversation, Starter=userTwo,
                                                                         Receiver=userOne)
        return conversation


# Zur delete Cascade: Ich bin mir nicht sicher, ob das wirklich so sinnvoll ist.
# Die Frage ist, was bringen Nachrichten an einen nicht existierenden User -> Verhalten muss noch definiert werden.
class Message(models.Model):
    From  = models.ForeignKey(User,on_delete=models.CASCADE,null=False,related_name='From')
    To = models.ForeignKey(User,on_delete=models.CASCADE,null=False,related_name='To')
    Text = models.TextField(max_length=5000,null=False)
    SendTime = models.DateTimeField(default=timezone.now)
    Conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=False, related_name='Conversation')
