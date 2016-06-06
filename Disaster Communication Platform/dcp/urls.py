from django.conf.urls import url
from dcp.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static

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
    url(r'^suchen/materielles/$', SearchMaterialView.as_view()),
    url(r'^suchen/immaterielles/$', SearchImmaterialView.as_view()),
    url(r'^suchen/personen/$', Suchen_Personen.as_view()),

    # Bieten
    url(r'^bieten/$', Bieten.as_view()),
    url(r'^bieten/materielles/$', OfferMaterialView.as_view()),
    url(r'^bieten/immaterielles/$', OfferImmaterialView.as_view()),

    # Chat
    url(r'^chat/$', Chat.as_view(), name='Chat'),
    url(r'^profil/netzwerke/$',ChatOverview.as_view(),name='ChatOverview'),
    # AdminPanel
    url(r'^administator/$',userAdminOverview.as_view(),name='UserAdminOverview'),
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
    #Profil
    url(r'^profil/$', MyProfile.as_view()),
    url(r'^profil/bearbeiten/$', EditProfile.as_view())

]

# media url patters
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)