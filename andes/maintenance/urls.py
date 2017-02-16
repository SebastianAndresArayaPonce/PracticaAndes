from django.conf.urls import url
from wkhtmltopdf.views import PDFTemplateView

from . import views

app_name = 'maintenance'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^pdf/$', PDFTemplateView.as_view(template_name='maintenance/index.html', filename='my_pdf.pdf'), name='pdf'),
    url(r'^guideline/machine/(?P<machine_number>[0-9]+)/level/(?P<level>[0-9]+)/$', views.guideline, name="guideline"),
    url(r'^workorder/(?P<workorder_number>[0-9]+)$', views.workorder, name="workorder"),
    url(r'^workorder/(?P<workorder_number>[0-9]+)/confirm$', views.confirm_workorder, name="confirm_workorder"),
    url(r'^workorder$', views.process_workorder, name="process_workorder"),
    url(r'^workdescription/(?P<suffix>[0-9]+)$', views.get_work_description, name="work_description"),
    url(r'^sparepartlist/(?P<suffix>[0-9]+)$', views.get_spare_part_list, name="spare_part_list"),
    url(r'^spareparttype/(?P<id>[0-9]+)$', views.get_spare_part_type, name="spare_part_type"),
    url(r'^inputlist/(?P<suffix>[0-9]+)$', views.get_input_list, name="input_list"),
]
