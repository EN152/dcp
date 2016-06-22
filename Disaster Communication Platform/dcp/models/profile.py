from .imports import *
from .catastrophe import *
from .government import *
from .ngo import *

class Profile(models.Model): # Wir erweitern das User Modell, wie es hier beschrieben wird:https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#extending-the-existing-user-model
    user = models.OneToOneField(User)
    currentCatastrophe = models.ForeignKey(Catastrophe,related_name='currentCatastrophe',null=True,blank=True) # TODO: Kaskade?
    ngo = models.ForeignKey(Ngo, on_delete=models.DO_NOTHING, null=True)
    government = models.ForeignKey(Government, on_delete=models.DO_NOTHING, null=True)
    is_organization_admin = models.BooleanField(default=False, null=False)
    date_joined_organization = models.DateTimeField(default=timezone.now)

    def setOrganizationAdmin(self, organitationAdmin):
        self.is_organization_admin = organitationAdmin
        self.save()

    def resetOrganization(self):
        """
        Setzt NGO und Government auf null zurück
        :author: Jasper
        :return: False falls nicht erfolgreich, True falls erfolgreich
        """
        self.ngo = None
        self.government = None
        self.is_organization_admin = False
        self.save()

    def acceptNgoInviteById(self, ngoId):
        """
        Setzt eine neue Ngo
        :author: Jasper
        :param ngoId: Die Id der neuen Ngo
        :return: False falls nicht erfolgreich, True falls erfolgreich
        """
        if ngoId is None: # Mache nichts
            return False
        try:
            ngoId = int(ngoId)
        except ValueError: #  ngoId kein Int
            return False
        ngo = get_object_or_none(Ngo,id=ngoId)
        invite = get_object_or_none(Invite_Ngo,user=self.user,organization=ngo)
        if ngo is None or invite is None:
            return False
        else:
            self.government = None
            self.ngo = ngo
            self.isOrganziationAdmin = False
            self.date_joined_organization = timezone.now()
            self.save()
            invite.delete()
            return True

    def acceptGovernmentInviteById(self, governmentId):
        """
        Setzt ein neues Government
        :author: Jasper
        :param ngoId: Die Id des neuen Government
        :return: False falls nicht erfolgreich, True falls erfolgreich
        """
        if governmentId is None: # Mache nichts
            return False
        try:
            governmentId = int(governmentId)
        except ValueError: #  ngoId kein Int
            return False
        government = get_object_or_none(Government,id=governmentId)
        invite = get_object_or_none(Invite_Government,user=self.user,organization=government)
        if government is None or invite is None:
            return False
        else:
            self.government = government
            self.ngo = None
            self.isOrganziationAdmin = False
            self.date_joined_organization = timezone.now()
            self.save()
            invite.delete()
            return True

    def getInvites(self):
        """
        Gibt eine Liste von den Invites zurück
        :author: Jasper
        :return: Eine Liste mit allen Invites
        """
        from dcp.customclasses.Helpers import getInvites
        return getInvites(user=self.user)
    
    def getOrganization(self):
        if self.ngo is not None:
            return self.ngo
        elif self.government is not None:
            return self.government
        else:
            return None

    def setCatastropheById(self,catId):
        """
        Setzt eine neue Katastrophe
        :author: Vincent
        :param catId: Die Id der neuen Katastrophe
        :return: False falls nicht erfolgreich, True falls erfolgreich
        """
        if catId is None: # Mache nichts
            return False
        try:
            catId = int(catId)
        except ValueError: #  catId kein Int
            return False
        newCatastrophe = get_object_or_none(Catastrophe,id=catId)
        if newCatastrophe is None:
            return False
        else:
            self.currentCatastrophe = newCatastrophe
            return True

    def get_profile_or_none(user: User):
            """
            Hole das Profil eines Benutzers
            Sonderfall Anonymous Benutzer: Default Profile
            :param user: Der Benutzer, dessen Profil man erfragen will
            :return: Das Profil des Benutzers, falls existent, sonst None
            """
            if user.is_anonymous():
                return Profile(currentCatastrophe=None)
            if user is None:
                return None
            else:
                return get_object_or_none(Profile, user=user)
    def get_profile_or_create(user: User):
        """
        Hole das Profil eines Benutzers oder erstelle es, falls er noch keins hat
        :param user: Der Benutzer, dessen Profil man erstellen will
        :return: None falls Fehler, sonst das Profil
        """
        if user.is_anonymous():
            return Profile(currentCatastrophe=None)
        if user is None:
            return None
        else:
            p = Profile.get_profile_or_none(user)
            if p is None:
                p = Profile(user=user,currentCatastrophe=None)
                p.save()
            return p

def create_profile(sender, **kwargs):
    """
    Zusammen mit post_save wird immer ein Profil erstellt,
    wenn ein Nutzer erstellt wird
    Siehe hier: https://blog.khophi.co/extending-django-user-model-userprofile-like-a-pro/
    :param sender:
    :param kwargs:
    :return:
    """
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)

class Invite_Ngo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    organization = models.ForeignKey(Ngo, on_delete=models.CASCADE, null=False)
    date_created = models.DateTimeField(default=timezone.now)

    def getInviteType(self):
        return 'Invite_Ngo'

class Invite_Government(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    organization = models.ForeignKey(Government, on_delete=models.CASCADE, null=False)
    date_created = models.DateTimeField(default=timezone.now)

    def getInviteType(self):
        return 'Invite_Government'

class Comment_Relation(models.Model):
    class Meta:
        abstract = False

class Comment(models.Model):
    relation = models.ForeignKey(Comment_Relation, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    created_date = models.DateTimeField(default=timezone.now)
    text = models.TextField(max_length=500, null=False)

    def __unicode__(self):
        return self.text