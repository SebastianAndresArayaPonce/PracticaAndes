from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from . import views

app_name = 'maintenance'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^workorder/(?P<workorder_number>[0-9]+)$', views.workorder, name="workorder"),
    url(r'^workorder/(?P<workorder_number>[0-9]+)/process', views.process_workorder, name="process_workorder"),
    url(r'^workdescription/(?P<suffix>[0-9]+)$', views.get_work_description, name="work_description"),
    url(r'^sparepartlist/(?P<suffix>[0-9]+)$', views.get_spare_part_list, name="spare_part_list"),
    url(r'^spareparttype/(?P<id>[0-9]+)$', views.get_spare_part_type, name="spare_part_type"),
    url(r'^inputlist/(?P<suffix>[0-9]+)$', views.get_input_list, name="input_list"),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
