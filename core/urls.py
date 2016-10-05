from django.conf.urls import url

from core import views

urlpatterns = [
    url(r'^$', views.index, name='core.views.index'),
    url(r'^add/$', views.add, name='core.views.add'),
    url(r'^accounts/login/$', views.login_user, name='core.views.login_user'),
    url(r'^csv/(?P<slug>[\w\-]+)/$', views.csv,name="core.views.csv"),
]