from django.conf.urls import url

from core import views

urlpatterns = [
    url(r'^$', views.index, name='core.views.index'),
    url(r'^edit/(?P<year>\d{4})/$', views.edit, name='core.views.edit'),
    url(r'^accounts/login/$', views.login_user, name='core.views.login_user'),
    url(r'^csv/(?P<slug>[\w\-]+)/$', views.csv,name="core.views.csv"),
    url(r'^csv_all/$', views.csv_all,name="core.views.csv_all"),
]