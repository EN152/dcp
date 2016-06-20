from .imports import *

class Catastrophe(models.Model):
    Title = models.CharField(max_length=200)
    Location = models.CharField(max_length=100) # Soll das so? Nicht per Map Anzeigen?r
    PubDate = models.DateTimeField('date published', default=timezone.now)
    def __unicode__(self):
        return self.Title
    def isAbleToEdit(self,user : User):
        """
        Gibt zurück, ob ein Benutzer eine Katastrophe bearbeiten darf oder nicht
        :param user: Der Benutzer, der erfragt
        :return: True falls er darf, False falls nciht
        """
        return user.has_perm('dcp.EditCatastrophe')
    class Meta:
            permissions = (
                ("EditCatastrophe","Kann eine Katastrophe editieren/löschen"),
                ("CreateCatastrophe","Kann eine Katastrophe erstellen"),
            )
            unique_together = ('Title','Location')
