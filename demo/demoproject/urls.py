from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from . import views

home = TemplateView.as_view(template_name='home.html')

urlpatterns = patterns(
    '',
    url(r'^$', home, name='home'),
    url(r'^colors/$', views.colors, name='colors'),
    url(r'^line_chart/$', views.line_chart, name='line_chart'),
    url(r'^line_chart/json/$', views.line_chart_json, name='line_chart_json'),
)
