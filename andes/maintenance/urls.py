from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<machine_number>[0-9]+)/(?P<level>[0-9]+)/guideline/$', views.guideline, name="guideline"),
    url(r'^ot/$', views.ot, name="ot"),
]
