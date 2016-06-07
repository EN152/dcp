
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

