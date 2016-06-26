from .imports import *
from django.db import models
from .catastrophe import *
from .organizations import *

class Profile(models.Model): # Wir erweitern das User Modell, wie es hier beschrieben wird:https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#extending-the-existing-user-model
    user = models.OneToOneField(User)
    currentCatastrophe = models.ForeignKey(Catastrophe, related_name='currentCatastrophe', null=True,blank=True)
    ngo = models.ManyToManyField(Ngo, through='NgoMember')
    government = models.ManyToManyField(Government, through='GovernmentMember')
    show_map = models.BooleanField(default=True, null=False)
    show_picture = models.BooleanField(default=True, null=False)

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

class Invite(models.Model):
    created_date = models.DateTimeField(default=timezone.now)

class NgoInvite(Invite):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    organization = models.ForeignKey(Ngo, on_delete=models.CASCADE, null=False)

    def acceptInvite(self):
        membership, created = NgoMember.objects.get_or_create(profile=self.profile, ngo=self.organization)
        self.delete()
        return membership

    class Meta:
         unique_together = ('profile','organization')

class GovernmentInvite(Invite):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    organization = models.ForeignKey(Government, on_delete=models.CASCADE, null=False)

    def acceptInvite(self):
        membership, created = GovernmentMember.objects.get_or_create(profile=self.profile, government=self.organization)
        self.delete()
        return membership

    class Meta:
         unique_together = ('profile','organization')

class Comment_Relation(models.Model):
    pass

class Comment(models.Model):
    relation = models.ForeignKey(Comment_Relation, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    created_date = models.DateTimeField(default=timezone.now)
    text = models.TextField(max_length=500, null=False)

    def __unicode__(self):
        return self.text

    def __str__(self):
        return self.text

class Member(models.Model):
    isOrganizationAdmin = models.BooleanField(default=False, null=False)
    isAreaAdmin = models.BooleanField(default=False, null=False)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = False

class NgoMember(Member):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    ngo = models.ForeignKey(Ngo, on_delete=models.CASCADE, null=False)

    class Meta:
         unique_together = ('profile','ngo')

class GovernmentMember(Member):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    government = models.ForeignKey(Government, on_delete=models.CASCADE, null=False)

    class Meta:
         unique_together = ('profile','government')