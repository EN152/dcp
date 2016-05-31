from django.conf.urls import url
from dcp.views import *

urlpatterns = [
    url(r'^$', Index.as_view()),

    # Spezialseiten
    url(r'^anmelden/$', Login.as_view()),
    url(r'^abmelden/$', Logout.as_view()),
    url(r'^registrieren/$', Register.as_view()),

    # Karten
    url(r'^orte/karten/$', Karten.as_view()),

    # Suchen
    url(r'^suchen/$', Suchen.as_view()),
    url(r'^suchen/materielles/$', Suchen_Materielles.as_view()),
    url(r'^suchen/immaterielles/$', Suchen_Immaterielles.as_view()),
    url(r'^suchen/personen/$', Suchen_Personen.as_view()),
    # Chat
    url(r'^chat/$', Chat.as_view(), name='Chat'),
    url(r'^profil/netzwerke',Overview.as_view(),name='ChatOverview')
#    # Bieten
#    url(r'^bieten/$', views.bieten),
#    url(r'^bieten/materielles/$', views.bieten_materielles),
#    url(r'^bieten/immmaterielles/$', views.bieten_immaterielles),
#
#    # Wissen
#    url(r'^wissen/$', views.wissen),
#    url(r'^wissen/neuigkeiten/$', views.wissen_neuigkeiten),
#    url(r'^wissen/gefahren/$', views.wissen_gefahren),
#    url(r'^wissen/fragen/$', views.wissen_fragen),
#    url(r'^wissen/abstimmungen/$', views.wissen_abstimmungen),
#    url(r'^wissen/archiv/$', views.wissen_archiv),
#
#    # Orte
#    url(r'^orte/$', views.orte),
#    url(r'^orte/anlaufstellen/$', views.orte_anlaufstellen),
#    url(r'^orte/karten/$', views.orte_karten),
#    url(r'^orte/fotos/$', views.orte_fotos),
#
    #Profil
    url(r'^profil/$', MyProfile.as_view()),
    url(r'^profil/bearbeiten/$', EditProfile.as_view())
#    url(r'^profil/daten/$', views.profil_daten),
#    url(r'^profil/netzwerke/$', views.profil_netzwerke),

]