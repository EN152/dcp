from django.conf.urls import url
from dcp.views import *

urlpatterns = [
<<<<<<< HEAD
    url(r'^$', views.index, name='index'),
    url(r'^imprint/$', views.imprint, name='imprint'),
    url(r'^login/$', views.Login),
    url(r'^logout/$', views.Logout),
    url(r'^register/$', views.register),
=======
    url(r'^$', Index.as_view()),
    
    # Spezialseiten
    url(r'^login/$', Login.as_view()),
   # url(r'^administration/$', views.administration),
   # url(r'^suchergebnisse/$', views.suchergebnisse),

    # Suchen
    url(r'^suchen/$', Suchen.as_view()),
    url(r'^suchen/materielles/$', Suchen_Materielles.as_view()),
    url(r'^suchen/immaterielles/$', Suchen_Immaterielles.as_view()),
    url(r'^suchen/personen/$', Suchen_Personen.as_view()),

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
#    # Profil
#    url(r'^profil/$', views.profil),
#    url(r'^profil/daten/$', views.profil_daten),
#    url(r'^profil/netzwerke/$', views.profil_netzwerke),

>>>>>>> e708912534f66164aa2c8e1a84d33a7daecb4a99
]