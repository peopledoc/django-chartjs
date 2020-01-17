from pkg_resources import parse_version
import django
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

django_version = parse_version(django.get_version())
if django_version <= parse_version("1.9"):
    from django.conf.urls import patterns

home = TemplateView.as_view(template_name="home.html")

patterns_list = [
    url(r"^$", home, name="home"),
    url(r"^colors/$", views.colors, name="colors"),
    # Column
    url(
        r"^column_highchart/json/$",
        views.column_highchart_json,
        name="column_highchart_json",
    ),
    # Line chart
    url(r"^line_chart/$", views.line_chart, name="line_chart"),
    url(r"^line_chart/json/$", views.line_chart_json, name="line_chart_json"),
    url(
        r"^line_chart/discontinuous/json/$",
        views.discontinuous_dates_chart_json,
        name="discontinuous_line_chart_json",
    ),
    url(
        r"^line_chart/options/$",
        views.line_chart_with_options,
        name="line_chart_with_options",
    ),
    url(
        r"^line_highchart/json/$", views.line_highchart_json, name="line_highchart_json"
    ),
    url(
        r"^line_highchart/discontinuous/json/$",
        views.discontinuous_dates_highchart_json,
        name="discontinuous_line_highchart_json",
    ),
    # Pie
    url(r"^pie_highchart/json/$", views.pie_highchart_json, name="pie_highchart_json"),
    url(
        r"^donut_highchart/json/$",
        views.donut_highchart_json,
        name="donut_highchart_json",
    ),
]

if django_version <= parse_version("1.9"):
    urlpatterns = patterns("", *patterns_list)
else:
    urlpatterns = patterns_list
