from django.conf.urls import url
from dcp.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static
from django.conf import  settings

urlpatterns = [
    # Core
    url(r'^$', Index.as_view(),name='Index'),
    url(r'^catastrophechange/$', CatastropheChangeView.as_view(),name='CatastropheChangeView'),

    # Spezialseiten
    url(r'^anmelden/$', LoginView.as_view()),
    url(r'^abmelden/$', LogoutView.as_view()),

    # Suchen
    url(r'^suchen/$', Suchen.as_view()),
    url(r'^suchen/materielles/$', SearchMaterialView.as_view(),name='SearchMaterialView'),
    url(r'^suchen/immaterielles/$', SearchImmaterialView.as_view(),name='SearchImmaterialView'),
    url(r'^suchen/personen/$', Suchen_Personen.as_view()),
    url(r'^suchen/wortsuche/$', WordSearch.as_view(), name='WordSearch'),

    # Bieten
    url(r'^bieten/$', Bieten.as_view()),
    url(r'^bieten/materielles/$', OfferMaterialView.as_view(),name='OfferMaterialView'),
    url(r'^bieten/immaterielles/$', OfferImmaterialView.as_view(),name='OfferImmaterialView'),

    # Chat
    url(r'^chat/$', Chat.as_view(), name='Chat'),
    url(r'^nachrichten/$',ChatOverview.as_view(),name='ChatOverview'),
    #url(r'^profil/netzwerke/$',ChatOverview.as_view(),name='ChatOverview'),

    # AdminPanel
    url(r'^administator/useroverview/$',UserAdminOverview.as_view(),name='UserAdminOverview'),
    url(r'^adminstrator/edituser/(?P<pk>\d+)/$', AdminEditUserProfileView.as_view(),name='AdminEditUserProfileView'),
    url(r'^administrator/deleteuser/(?P<pk>\d+)/$',DeleteUserView.as_view(),name='DeleteUserView'),
    url(r'^administrator/editcatastrophe/(?P<pk>\d+)/$',CatastropheEditView.as_view(),name='EditCatastropheView'),
    url(r'^administrator/catoverview/$',CatastropheOverviewView.as_view(),name='CatastropheOverview'),
    url(r'^administrator/ngomanager/$',NgoManagerView.as_view(),name='NgoManagerView'),
    url(r'^administrator/governmentmanager/$',GovernmentManagerView.as_view(),name='GovernmentManagerView'),
    url(r'^administrator/categorygoodmanager/$',CategorysGoodsMangerView.as_view(),name='CategoryGoodManagerView'),
    url(r'^administrator/timelinemanager/$',TimelineManagerView.as_view(),name='TimelineManagerView'),
    url(r'^administrator/areaadministrator/$',AreaAdminView.as_view(),name='AreaAdministratorView'),

    # Organisationen
    url(r'^ngo/(?P<pk>\d+)/$', NgoView.as_view(), name='NgoView'),
    url(r'^government/(?P<pk>\d+)/$', GovernmentView.as_view(),name='GovernmentView'),
    url(r'^area/(?P<pk>\d+)/$', AreaView.as_view(),name='AreaView'),
    
    # Orte
    url(r'^orte/karten/$', Karten.as_view()),

    # Wissen
    url(r'^wissen/$', Wissen.as_view(), name='Wissen'),
    url(r'^wissen/neuigkeiten/$', Neuigkeiten.as_view(), name='Wissen'),
    url(r'^wissen/neuigkeiten/bearbeiten/$', NeuigkeitenBearbeiten.as_view(), name='WissenBearbeiten'),
    url(r'^wissen/neuigkeiten/ansehen/$', NeuigkeitenAnsehen.as_view(), name='WissenAnsehen'),
    url(r'^wissen/neuigkeiten/anlegen/$', NeuigkeitenAnlegen.as_view(), name='WissenAnlegen'),
    url(r'^wissen/fragen/$', PostQuestionView.as_view()),
    url(r'^wissen/abstimmungen/$', PollsView.as_view(), name = 'PollsView'),

    # Aktionen
    url(r'^aktionen/$', Aktionen.as_view()),
    url(r'^aktionen/planung/$', AktionenPlanung.as_view()),
    url(r'^aktionen/laufende/$', AktionenLaufende.as_view(),name='EventsView'),


    #Profil
    url(r'^profil/$', Profil.as_view(), name='Profil'),
    url(r'^profil/daten/$', MyProfile.as_view(), name='ProfileView'),
    url(r'^profil/bearbeiten/$', EditProfile.as_view()),

    #Benachrichtigungen
    url(r'^notifications/$', NotificationView.as_view(), name='Notifications'),
]

# media url patters
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
