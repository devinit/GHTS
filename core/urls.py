from django.conf.urls import url

from core import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^csv/(?P<slug>[\w\-]+)/$', views.csv,name="core.views.csv"),
]