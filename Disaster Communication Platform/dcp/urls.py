from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^imprint/$', views.imprint, name='imprint'),
    url(r'^login/$', views.Login),
    url(r'^logout/$', views.Logout),
    url(r'^register/$', views.register),
]