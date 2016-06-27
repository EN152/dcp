from django.conf.urls import url
from dcp.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static
from django.conf import  settings

urlpatterns = [
    url(r'^$', Index.as_view(),name='Index'),

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
    url(r'^suchen/wortsuche/$', WordSearch.as_view(), name='WordSearch'),

    # Bieten
    url(r'^bieten/$', Bieten.as_view()),
    url(r'^bieten/materielles/$', OfferMaterialView.as_view()),
    url(r'^bieten/immaterielles/$', OfferImmaterialView.as_view()),

    # Chat
    url(r'^chat/$', Chat.as_view(), name='Chat'),
    url(r'^nachrichten/$',ChatOverview.as_view(),name='ChatOverview'),
    #url(r'^profil/netzwerke/$',ChatOverview.as_view(),name='ChatOverview'),
    
    # AdminPanel
    url(r'^administator/useroverview/$',UserAdminOverview.as_view(),name='UserAdminOverview'),
    url(r'^adminstrator/edituser/(?P<pk>\d+)/$', AdminEditUserProfileView.as_view(),name='AdminEditUserProfileView'),
    url(r'^administrator/deleteuser/(?P<pk>\d+)/$',DeleteUserView.as_view(),name='DeleteUserView'),
    url(r'^administrator/createcat/$',CreateCatastrophe.as_view(),name='CreateOrEditCatastrophe'),
    url(r'^administrator/catoverview/$',CatastropheOverview.as_view(),name='CatastropheOverview'),
    url(r'^administrator/catdelete/(?P<pk>\d+)/$',DeleteCatastropheView.as_view(),name='DeleteCatastropheView'),
    url(r'^administrator/ngomanager/$',NgoManagerView.as_view(),name='NgoManagerView'),
    url(r'^administrator/governmentmanager/$',GovernmentManagerView.as_view(),name='GovernmentManagerView'),
    url(r'^administrator/categorygoodmanager/$',CategorysGoodsMangerView.as_view(),name='CategoryGoodManagerView'),
    url(r'^administrator/areaadministrator/$',AreaAdminView.as_view(),name='AreaAdministratorView'),

    # Organisationen
    url(r'^ngo/(?P<pk>\d+)/$', NgoView.as_view(), name='NgoView'),
    url(r'^government/(?P<pk>\d+)/$', GovernmentView.as_view(),name='GovernmentView'),
    url(r'^area/(?P<pk>\d+)/$', AreaView.as_view(),name='AreaView'),

#    # Wissen
    url(r'^wissen/$', Wissen.as_view()),
    url(r'^wissen/neuigkeiten/$', PostNewsView.as_view()),
#   url(r'^wissen/gefahren/$', views.wissen_gefahren),
#    url(r'^wissen/fragen/$', views.wissen_fragen),
#    url(r'^wissen/abstimmungen/$', views.wissen_abstimmungen),
#    url(r'^wissen/archiv/$', views.wissen_archiv),

    # Aktionen
    url(r'^aktionen/planung/$', AktionenPlanung.as_view()),
    url(r'^aktionen/laufende/$', AktionenLaufende.as_view()),


#    # Orte
#    url(r'^orte/$', views.orte),
#    url(r'^orte/anlaufstellen/$', views.orte_anlaufstellen),
#    url(r'^orte/karten/$', views.orte_karten),
#    url(r'^orte/fotos/$', views.orte_fotos),

    #Profil
    url(r'^profil/$', MyProfile.as_view(), name='ProfileView'),
    url(r'^profil/bearbeiten/$', EditProfile.as_view()),
]

# media url patters
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)