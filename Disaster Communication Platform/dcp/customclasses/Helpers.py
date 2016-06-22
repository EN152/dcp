# -*- coding: utf-8 -*-
from django.utils.http import urlencode
'''
Vincent: Resourcen Strings, für wiederverwendte Texte, Links usw.
'''
LOGIN_URL = '/anmelden'
PleaseEnterMessageString = 'Bitte eine Nachricht eingeben'
ChatWithString = 'Chat mit'
'''
Vincent: Funktionen, die immer wieder benutzt werden
'''
sessionStringCatastrophe = "CatastropheId"



def get_object_or_none(model, **kwargs):
    """
    Gibt entweder das Objekt, oder ansonten None zurück
    :param model: Das zu durchsuchende Datenbankmodell
    :param kwargs: Die Parameter, die an die Query models.object.get gesendet werden soll
    :return: Das Objekt, falls existent, ansonsten null
    :raises keyError: Exception, falls mehr als ein Objekt existiert
    :author Vincent Ulitzsch
    """

    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
def url_with_querystring(path, **kwargs): #TODO: Refactor nach Helpers.
    return path + '?' + urlencode(kwargs)

def getInvites(user=None, ngo=None, government=None):
    """
    Liste von den gewünschten Invites, wobei immer nur der erste Parameter ausgeführt wird
    :author: Jasper
    :param user: User für den die Invites zurückgebenen werden sollen
    :param ngo: NGO für den die Invites zurückgebenen werden sollen
    :param government: Government für den die Invites zurückgebenen werden sollen
    :return: Liste von allen gefunden Invites
    """
    invites = []
    from dcp.models.profile import Invite_Government
    from dcp.models.profile import Invite_Ngo
    if user != None:
        for invite in Invite_Ngo.objects.filter(user = user):
            invites.append(invite)
        for invite in Invite_Government.objects.filter(user = user):
            invites.append(invite)
    elif ngo != None:
        invites = Invite_Ngo.objects.filter(organization = ngo)
    elif government != None:
        invites = Invite_Government.objects.filter(organization = government)
    else:
        for invite in Invite_Ngo.objects.all():
            invites.append(invite)
        for invite in Invite_Government.objects.all():
            invites.append(invite)
    return sorted(invites, key=lambda i: i.date_created, reverse=True)
