from django.conf.urls import url

from . import views

app_name = 'maintenance'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^guideline/machine/(?P<machine_number>[0-9]+)/level/(?P<level>[0-9]+)/$', views.guideline, name="guideline"),
    url(r'^workorder/(?P<workorder_number>[0-9]+)$', views.workorder, name="workorder"),
    url(r'^workorder/(?P<workorder_number>[0-9]+)/confirm$', views.confirm_workorder, name="confirm_workorder"),
    url(r'^workorder$', views.process_workorder, name="process_workorder"),
]
