from .imports import *
from dcp import dcpSettings
from dcp.models.organizations import Government, Ngo

class Catastrophe(models.Model):
    title = models.CharField(max_length=200)
    locationString = models.CharField(max_length=100) # Soll das so? Ja. Wird der reverse aus x und y drin gespeichert und muss nicht jedesml neu aufgelöst werden
    date_created = models.DateTimeField('date published', default=timezone.now)
    location_x = models.FloatField(null=False, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    location_y = models.FloatField(null=False, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    radius = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(dcpSettings.CATASTROPHE_MAX_RADIUS)])
    maxOutsideRadius = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(dcpSettings.CATASTROPHE_MAX_RADIUS)])
    # Fully catastrophes manager
    ngos = models.ManyToManyField(Ngo, related_name='catastrophes')
    governments = models.ManyToManyField(Government, related_name='catastrophes')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def isAbleToEdit(self, user : User):
        """
        Gibt zurück, ob ein Benutzer eine Katastrophe bearbeiten darf oder nicht
        :author: Jasper
        :param user: Der Benutzer, der erfragt
        :return: True falls er darf, False falls nciht
        """
        from dcp.auth.catastropheAuth import isCatastropheAdmin
        return isCatastropheAdmin(user.profile, self)

    class Meta:
            permissions = (
                ("EditCatastrophe","Kann eine Katastrophe editieren/löschen"),
                ("CreateCatastrophe","Kann eine Katastrophe erstellen"),
            )
            unique_together = ('title','locationString')
