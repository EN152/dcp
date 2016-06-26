from .imports import *
from dcp import dcpSettings

class Catastrophe(models.Model):
    title = models.CharField(max_length=200)
    locationString = models.CharField(max_length=100) # Soll das so? Nicht per Map Anzeigen?r
    date_created = models.DateTimeField('date published', default=timezone.now)
    location_x = models.FloatField(null=False, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    location_y = models.FloatField(null=False, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    radius = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(dcpSettings.CATASTROPHE_MAX_RADIUS)])

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

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
            unique_together = ('title','locationString')
