from django.conf.urls import url
from dcp.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static

urlpatterns = [
    url(r'^$', Index.as_view()),

    # Spezialseiten
    url(r'^login/$', Login.as_view()),
    url(r'^logout/$', Logout.as_view()),
    url(r'^register/$', Register.as_view()),
# url(r'^administration/$', views.administration),
# url(r'^suchergebnisse/$', views.suchergebnisse),

    # Suchen
    url(r'^suchen/$', Suchen.as_view()),
    url(r'^suchen/materielles/$', Suchen_Materielles.as_view()),
    url(r'^suchen/immaterielles/$', Suchen_Immaterielles.as_view()),
    url(r'^suchen/personen/$', Suchen_Personen.as_view()),

    # Bieten
    url(r'^bieten/$', Bieten.as_view()),
    url(r'^bieten/materielles/$', Bieten_Materielles.as_view()),
    url(r'^bieten/immaterielles/$', Bieten_Immaterielles.as_view()),

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

]

# media url patters
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)